from dataclasses import dataclass, field
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from em_timeseries.grid import TimeRange, TimeSeriesRun


@dataclass(frozen=True)
class DeliveryWindow:
    """The delivery period a decision covers (start inclusive, end exclusive)."""

    start: datetime

    end: datetime

    @classmethod
    def next_delivery_day(
        cls,
        from_ts: datetime,
        tz_name: str,
    ) -> "DeliveryWindow":
        """The next full delivery day after from_ts in the given zone.

        Day boundaries are computed as local midnights, so the window
        spans 23/24/25 hours across DST transitions.
        """
        tz = ZoneInfo(tz_name)
        local = from_ts.astimezone(tz)
        next_date = local.date() + timedelta(days=1)
        end_date = next_date + timedelta(days=1)

        start = datetime(
            next_date.year, next_date.month, next_date.day,
            tzinfo=tz,
        )
        end = datetime(
            end_date.year, end_date.month, end_date.day,
            tzinfo=tz,
        )

        return cls(start=start, end=end)

    @property
    def duration_seconds(self) -> int:
        return int(TimeRange.duration(self.start, self.end).total_seconds())

    @property
    def hours(self) -> int:
        return int(self.duration_seconds // 3600)


@dataclass(frozen=True)
class ProductionForecastInput:
    """A production forecast fetched for the decision's portfolio.

    forecast_id references the forecast-service object (a plain id — the
    object lives in another service's database).
    """

    forecast_id: int | None = None

    run: TimeSeriesRun | None = None


@dataclass(frozen=True)
class PriceForecastInput:
    """A market price forecast fetched for the decision's market."""

    forecast_id: int | None = None

    run: TimeSeriesRun | None = None


@dataclass(frozen=True)
class StorageContext:
    """Battery storage state relevant to the decision (charge level, free
    capacity, ...).

    Deliberately a placeholder: a real storage context is dynamic and
    cannot be served by a mere forecast. Structure exists so strategies
    can already declare and consume the requirement.
    """


@dataclass(frozen=True)
class GridConstraints:
    """Network/grid capacities constraining the portfolio's positions.

    Placeholder, same rationale as StorageContext.
    """


@dataclass
class DayAheadSalesDecisionRequest:
    """Everything a day-ahead sales strategy may work with.

    Fields the strategy did not declare a requirement for stay unset —
    strategies must handle "provider answered unavailable" gracefully.
    """

    portfolio_id: int

    delivery_window: DeliveryWindow

    market: str | None = None

    production_forecast: ProductionForecastInput | None = None

    price_forecast: PriceForecastInput | None = None

    storage_context: StorageContext | None = None

    grid_constraints: GridConstraints | None = None
