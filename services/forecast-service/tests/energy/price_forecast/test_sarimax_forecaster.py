from datetime import timedelta

import numpy as np
import pytest

from app.energy.price_forecast.sarimax.config import SarimaxConfig
from app.energy.price_forecast.sarimax.forecaster import (
    SarimaxPriceForecaster,
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


def test_forecast_fills_grid_with_prices():
    price_provider = FakeTimeSeriesProvider()
    forecaster = SarimaxPriceForecaster(
        market="DE-LU",
        price_provider=price_provider,
        config=sarimax_config(),
    )

    forecast = forecaster.forecast(market="DE-LU", horizon=timedelta(hours=24))

    assert forecast.market == "DE-LU"
    assert forecast.provider == PROVIDER_NAME
    assert forecast.run.resolution == SLOT
    assert forecast.run.slots == 24
    prices = [value.values[0] for value in forecast.time_series[0].values]
    assert len(prices) == 24
    assert all(price is not None and np.isfinite(price) for price in prices)

    past = price_provider.observed_requests[0]
    assert past.slots == 7 * 24
    assert isinstance(past, TimeRange)


def test_forecast_pulls_past_and_future_from_exogenous_providers():
    price_provider = FakeTimeSeriesProvider()
    exog_provider = FakeTimeSeriesProvider()
    forecaster = SarimaxPriceForecaster(
        market="DE-LU",
        price_provider=price_provider,
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


def test_forecast_validates_market_binding():
    forecaster = SarimaxPriceForecaster(
        market="DE-LU",
        price_provider=FakeTimeSeriesProvider(),
        config=sarimax_config(),
    )

    with pytest.raises(ValueError, match="market"):
        forecaster.forecast(market="FR", horizon=timedelta(hours=24))


def test_forecast_rejects_short_history():
    forecaster = SarimaxPriceForecaster(
        market="DE-LU",
        price_provider=FakeTimeSeriesProvider(),
        config=sarimax_config(history=timedelta(hours=12)),
    )

    with pytest.raises(ValueError, match="history"):
        forecaster.forecast(market="DE-LU", horizon=timedelta(hours=24))
