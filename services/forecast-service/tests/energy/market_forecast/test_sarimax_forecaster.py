from datetime import timedelta

import numpy as np
import pytest

from app.energy.market_forecast.core.domain import BasisRole
from app.energy.market_forecast.sarimax.config import SarimaxConfig
from app.energy.market_forecast.sarimax.forecaster import (
    SarimaxForecaster,
    PROVIDER_NAME,
)
from app.forecasting.enums import ForecastMetric
from app.timeseries.domain import TimeRange, TimeSeriesRun
from app.timeseries.grid import build_run
from app.timeseries.provider import TimeSeriesProvider

SLOT = timedelta(hours=1)
METRIC = ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE


class FakeTimeSeriesProvider(TimeSeriesProvider):
    """Serves the received window back on its grid with a deterministic
    daily-seasonal pattern, and records how it was queried."""

    def __init__(self):
        self.observed_requests = []
        self.forecast_requests = []

    def get_observed(self, time_range: TimeRange) -> TimeSeriesRun:
        self.observed_requests.append(time_range)
        return build_run(METRIC, time_range, self._values(time_range))

    def get_forecast(self, time_range: TimeRange) -> TimeSeriesRun:
        self.forecast_requests.append(time_range)
        return build_run(METRIC, time_range, self._values(time_range))

    @staticmethod
    def _values(time_range: TimeRange) -> list[float]:
        slot_seconds = int(time_range.resolution.total_seconds())
        counter = int(time_range.start.timestamp()) // slot_seconds
        values = []
        for _ in range(time_range.slots):
            hour_of_day = (counter // 3600) % 24
            values.append(10.0 + 5.0 * np.sin(2 * np.pi * hour_of_day / 24))
            counter += 1
        return values


def sarimax_config(**overrides) -> SarimaxConfig:
    base = dict(
        history=timedelta(days=7),
        resolution=SLOT,
        seasonal_order=(1, 0, 0, 24),
        order=(1, 0, 0),
    )
    base.update(overrides)
    return SarimaxConfig(**base)


def make_forecaster(exogenous: dict | None = None) -> SarimaxForecaster:
    return SarimaxForecaster(
        market="DE-LU",
        variable=METRIC,
        endogenous_provider=FakeTimeSeriesProvider(),
        exogenous_providers=exogenous or {},
        config=sarimax_config(),
    )


def test_forecast_fills_grid_with_prices():
    forecaster = make_forecaster()

    forecast = forecaster.forecast(market="DE-LU", horizon=timedelta(hours=24))

    assert forecast.market == "DE-LU"
    assert forecast.provider == PROVIDER_NAME
    assert forecast.variable == METRIC
    assert forecast.run.resolution == SLOT
    assert forecast.run.slots == 24
    prices = [value.values[0] for value in forecast.time_series[0].values]
    assert len(prices) == 24
    assert all(price is not None and np.isfinite(price) for price in prices)

    past = forecaster.endogenous_provider.observed_requests[0]
    assert past.slots == 7 * 24
    assert isinstance(past, TimeRange)


def test_forecast_carries_its_basis_runs():
    exog_provider = FakeTimeSeriesProvider()
    forecaster = SarimaxForecaster(
        market="DE-LU",
        variable=METRIC,
        endogenous_provider=FakeTimeSeriesProvider(),
        exogenous_providers={
            "temperature-0": exog_provider,
            "temperature-1": FakeTimeSeriesProvider(),
        },
        config=sarimax_config(),
    )

    forecast = forecaster.forecast(market="DE-LU", horizon=timedelta(hours=6))

    # one endogenous run plus one past and one future run per
    # exogenous provider
    assert len(forecast.basis) == 5
    endogenous = [
        item for item in forecast.basis
        if item.role == BasisRole.ENDOGENOUS
    ]
    assert len(endogenous) == 1
    assert endogenous[0].name == str(METRIC)
    assert endogenous[0].run.series.metric == METRIC
    assert endogenous[0].run.base.slots == 7 * 24

    exogenous_fit = [
        item for item in forecast.basis
        if item.role == BasisRole.EXOGENOUS and item.metadata["phase"] == "fit"
    ]
    exogenous_predict = [
        item for item in forecast.basis
        if item.role == BasisRole.EXOGENOUS and item.metadata["phase"] == "predict"
    ]
    assert [item.name for item in exogenous_fit] == ["temperature-0", "temperature-1"]
    assert all(item.run.base.slots == 6 for item in exogenous_predict)


def test_forecast_pulls_past_and_future_from_exogenous_providers():
    exog_provider = FakeTimeSeriesProvider()
    forecaster = SarimaxForecaster(
        market="DE-LU",
        variable=METRIC,
        endogenous_provider=FakeTimeSeriesProvider(),
        exogenous_providers={
            ForecastMetric.TEMPERATURE: exog_provider,
            ForecastMetric.TOTAL_ENERGY_CONSUMPTION: FakeTimeSeriesProvider(),
        },
        config=sarimax_config(),
    )

    forecast = forecaster.forecast(market="DE-LU", horizon=timedelta(hours=6))

    assert forecast.run.slots == 6
    assert len(exog_provider.observed_requests) == 1
    assert len(exog_provider.forecast_requests) == 1
    assert exog_provider.forecast_requests[0].slots == 6


def test_forecast_validates_market_and_variable_binding():
    forecaster = make_forecaster()

    with pytest.raises(ValueError, match="market"):
        forecaster.forecast(market="FR", horizon=timedelta(hours=24))

    with pytest.raises(ValueError, match="market"):
        forecaster.forecast(
            market="DE-LU",
            horizon=timedelta(hours=24),
            variable=ForecastMetric.ELECTRICITY_PRICE,
        )


def test_forecast_rejects_short_history():
    forecaster = SarimaxForecaster(
        market="DE-LU",
        variable=METRIC,
        endogenous_provider=FakeTimeSeriesProvider(),
        config=sarimax_config(history=timedelta(hours=12)),
    )

    with pytest.raises(ValueError, match="history"):
        forecaster.forecast(market="DE-LU", horizon=timedelta(hours=24))
