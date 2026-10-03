import math
from datetime import datetime, timedelta, timezone

import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

from app.energy.market_forecast.core.domain import (
    BasisRole,
    EnergyMarketForecast,
    ForecastBasis,
)
from app.energy.market_forecast.core.forecaster import EnergyMarketForecaster
from app.forecasting.enums import ForecastMetric
from app.energy.market_forecast.sarimax.config import SarimaxConfig
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series_value import TimeSeriesValue
from app.forecasting.encoding.definitions import ScalarDefinition
from app.timeseries.domain import TimeRange, TimeSeriesRun
from app.timeseries.provider import TimeSeriesProvider

PROVIDER_NAME = "sarimax"


class SarimaxForecaster(EnergyMarketForecaster):
    """A thin SARIMAX model wrapper.

    It gathers the endogenous past from one provider and, for every
    configured exogenous variable, past and future from that
    variable's own provider; fits the model and predicts the
    requested span. Everything beyond that — data sources, window
    policies, non-temporal context (market, location) — is handled by
    the factory composing the providers and by the providers
    themselves. The providers are market-, location- and
    variable-bound, so the forecaster is bound to exactly the market
    and variable passed at composition time; the forecast method
    validates both arguments against them.
    """

    def __init__(
        self,
        market: str,
        variable: ForecastMetric,
        endogenous_provider: TimeSeriesProvider,
        exogenous_providers: dict | None = None,
        config: SarimaxConfig = None,
    ):
        self.market = market
        self.variable = variable
        self.endogenous_provider = endogenous_provider
        self.exogenous_providers = exogenous_providers or {}
        self.config = config or SarimaxConfig()

    def forecast(
        self,
        market: str,
        horizon: timedelta,
        resolution: timedelta | None = None,
        variable: ForecastMetric = None,
    ) -> EnergyMarketForecast:
        variable = variable or self.variable
        if market != self.market or variable != self.variable:
            raise ValueError(
                f"This forecaster is composed for market {self.market} "
                f"and variable {self.variable}, "
                f"not for market {market} and variable {variable}"
            )
        resolution = resolution or self.config.resolution

        now = self._now_floor(resolution)
        slots = max(
            1,
            math.ceil(horizon.total_seconds() / resolution.total_seconds()),
        )
        history_slots = (
            int(self.config.history.total_seconds())
            // int(resolution.total_seconds())
        )
        past = TimeRange(
            start=now - resolution * history_slots,
            end=now,
            resolution=resolution,
        )
        future = TimeRange(
            start=now,
            end=now + resolution * slots,
            resolution=resolution,
        )

        endog_run = self.endogenous_provider.get_observed(past)
        endog = np.asarray(endog_run.series.values, dtype="float64")
        if len(endog) < self._features_needed():
            raise ValueError(
                f"Need at least {self._features_needed()} slots of history "
                f"for market {market}, got {len(endog)}"
            )

        exogenous, past_exog, future_exog = self._exog_matrix(past, future)

        return self._predict(
            endog,
            past_exog,
            future_exog,
            endog_run,
            exogenous,
            market,
            now,
            resolution,
            slots,
            metric=endog_run.series.metric,
        )

    # ------------------------------------------------------------------
    # exogenous matrix

    def _exog_matrix(
        self,
        past: TimeRange,
        future: TimeRange,
    ) -> tuple[list[tuple[str, TimeSeriesRun, TimeSeriesRun]],
               np.ndarray | None, np.ndarray | None]:
        """Gather past and future columns per exogenous provider."""
        exogenous = []
        past_columns = []
        future_columns = []
        for name, provider in self.exogenous_providers.items():
            past_run = provider.get_observed(past)
            future_run = provider.get_forecast(future)
            exogenous.append((name, past_run, future_run))
            past_columns.append(np.asarray(past_run.series.values, dtype="float64"))
            future_columns.append(
                np.asarray(future_run.series.values, dtype="float64")
            )
        return (
            exogenous,
            np.column_stack(past_columns) if past_columns else None,
            np.column_stack(future_columns) if future_columns else None,
        )

    # ------------------------------------------------------------------
    # prediction

    def _predict(
        self,
        endog: np.ndarray,
        past_exog: np.ndarray | None,
        future_exog: np.ndarray | None,
        endog_run: TimeSeriesRun,
        exogenous: list[tuple[str, TimeSeriesRun, TimeSeriesRun]],
        market: str,
        now: datetime,
        resolution: timedelta,
        slots: int,
        metric,
    ) -> EnergyMarketForecast:
        """Fit SARIMAX on the training window and predict the future slots."""
        model = SARIMAX(
            endog,
            exog=past_exog,
            order=self.config.order,
            seasonal_order=self.config.seasonal_order,
        )
        fitted = model.fit(disp=False)
        predicted = fitted.get_forecast(
            steps=slots, exog=future_exog,
        ).predicted_mean
        predicted = np.asarray(predicted, dtype="float64").ravel()

        basis = [
            ForecastBasis(
                run=endog_run,
                role=BasisRole.ENDOGENOUS,
                name=str(self.variable),
            ),
        ]
        for name, past_run, future_run in exogenous:
            basis.extend([
                ForecastBasis(
                    run=past_run,
                    role=BasisRole.EXOGENOUS,
                    name=name,
                    metadata={"phase": "fit"},
                ),
                ForecastBasis(
                    run=future_run,
                    role=BasisRole.EXOGENOUS,
                    name=name,
                    metadata={"phase": "predict"},
                ),
            ])

        return EnergyMarketForecast(
            market=market,
            provider=PROVIDER_NAME,
            run=TimeSeriesTimeBase(
                start=now,
                resolution=resolution,
                slots=slots,
            ),
            time_series=[
                TimeSeries(
                    metric=metric,
                    values=[TimeSeriesValue((float(value),)) for value in predicted],
                    value_definition=ScalarDefinition(),
                )
            ],
            basis=basis,
        )

    def _features_needed(self) -> int:
        return 2 * self.config.seasonal_order[3]

    @staticmethod
    def _now_floor(resolution: timedelta) -> datetime:
        """Floor the current time to the grid defined by resolution."""
        resolution_seconds = resolution.total_seconds()
        now = datetime.now(timezone.utc)
        return now - timedelta(seconds=now.timestamp() % resolution_seconds)
