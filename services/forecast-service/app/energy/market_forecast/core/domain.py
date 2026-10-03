from dataclasses import dataclass, field
from enum import StrEnum

from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.enums import ForecastMetric
from app.timeseries.domain import TimeSeriesRun


class BasisRole(StrEnum):
    """Role an input time series played in the forecast's model fit."""

    ENDOGENOUS = "endogenous"

    EXOGENOUS = "exogenous"


@dataclass(frozen=True)
class ForecastBasis:
    """One input time series a forecast's model consumed.

    Each basis run is the exact run (aligned values, interpolated
    where gaps were) that entered the model fit or prediction, so a
    stored forecast can be retraced to its factual inputs. `name`
    carries the composition-time series key of the forecaster's
    input slots (e.g. the predicted variable itself for the
    endogenous run, or "wind_speed-2" for an exogenous provider).
    """

    run: TimeSeriesRun

    role: BasisRole

    name: str

    metadata: dict | None = None


@dataclass(frozen=True)
class EnergyMarketForecast:
    """A forecast of an energy market variable (e.g. day-ahead price).

    market is a plain string (e.g. "DE-LU"). Forecast values are
    stored as scalar values: every returned series carries a
    ScalarDefinition, so each TimeSeriesValue holds exactly one value.
    `basis` holds the input runs the model consumed.
    """

    market: str

    provider: str

    run: TimeSeriesTimeBase

    time_series: list[TimeSeries]

    variable: ForecastMetric = ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE

    basis: list[ForecastBasis] = field(default_factory=list)
