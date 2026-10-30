"""Unit tests for the day-ahead sales decision plumbing.

Run inside the trading-service container (see CLAUDE.md). Pure domain /
alignment / strategy pieces; no HTTP and no Postgres.
"""

import datetime as dt

from em_timeseries.domain import TimeSeries, TimeSeriesTimeBase, TimeSeriesValue
from em_timeseries.encoding import QuantileDefinition, ScalarDefinition
from em_timeseries.grid import TimeSeriesRun

from app.decisions.alignment import delivery_grid, run_on_window
from app.decisions.request import DeliveryWindow
from app.decisions.requirements import Requirement, StrategyRequirements
from app.decisions.strategies.simple_conservative import (
    SimpleConservativeDayAheadSalesStrategy,
)

DEFAULT_DEFINITION = QuantileDefinition((5.0, 50.0, 95.0))


def _quantile_run(start, slots, p05, p50, p95):
    return TimeSeriesRun(
        base=TimeSeriesTimeBase(
            start=start,
            resolution=dt.timedelta(hours=1),
            slots=slots,
        ),
        series=TimeSeries(
            metric="active_power",
            values=[TimeSeriesValue.probabilistic(p05, p50, p95)] * slots,
            value_definition=DEFAULT_DEFINITION,
        ),
    )


def test_next_delivery_window_is_next_local_day():
    tz = "Europe/Berlin"
    from_ts = dt.datetime(2026, 3, 28, 14, 0, tzinfo=dt.timezone.utc)

    window = DeliveryWindow.next_delivery_day(from_ts=from_ts, tz_name=tz)

    # DST: 2026-03-29 02:00 -> 03:00 CET->CEST, delivery day has 23 hours.
    assert window.hours == 23
    assert window.start.hour == 0


def test_delivery_grid_spans_window():
    tz = "Europe/Berlin"
    window = DeliveryWindow.next_delivery_day(
        from_ts=dt.datetime(2026, 6, 1, 12, 0, tzinfo=dt.timezone.utc),
        tz_name=tz,
    )
    grid = delivery_grid(window)
    assert grid.slots == 24
    assert grid.resolution == dt.timedelta(hours=1)


def test_run_on_window_offsets_and_pads():
    # Forecast starts one hour before the delivery window and extends
    # beyond it: values must land offset; slots outside stay missing.
    tz = dt.timezone.utc
    window = DeliveryWindow(dt.datetime(2026, 6, 2, 10, 0, tzinfo=tz),
                            dt.datetime(2026, 6, 2, 13, 0, tzinfo=tz))
    run = _quantile_run(
        start=dt.datetime(2026, 6, 2, 8, 0, tzinfo=tz),
        slots=6,
        p05=5.0, p50=10.0, p95=15.0,
    )

    rebuilt = run_on_window(run, window)

    assert rebuilt.base.start == window.start
    assert rebuilt.base.slots == 3
    # Offset +2: window slot 0 corresponds to run slot index 2.
    assert rebuilt.series.values[0].values == (5.0, 10.0, 15.0)
    assert rebuilt.series.value_definition == DEFAULT_DEFINITION


def test_strategy_requirements_declare_named_requirements():
    requirements = StrategyRequirements.of(
        Requirement.PRICE_FORECAST,
        Requirement.PRODUCTION_FORECAST,
    )
    assert requirements.includes(Requirement.PRICE_FORECAST)
    assert not requirements.includes(Requirement.STORAGE_CONTEXT)


def test_simple_conservative_sells_p05():
    strategy = SimpleConservativeDayAheadSalesStrategy()

    from app.decisions.request import (
        DayAheadSalesDecisionRequest,
        PriceForecastInput,
        ProductionForecastInput,
    )

    tz = dt.timezone.utc
    window = DeliveryWindow(dt.datetime(2026, 6, 2, 0, 0, tzinfo=tz),
                            dt.datetime(2026, 6, 2, 3, 0, tzinfo=tz))
    run = _quantile_run(window.start, 3, p05=4.0, p50=8.0, p95=12.0)

    request = DayAheadSalesDecisionRequest(
        portfolio_id=7,
        delivery_window=window,
        market="DE-LU",
        production_forecast=ProductionForecastInput(forecast_id=11, run=run),
        price_forecast=PriceForecastInput(forecast_id=22, run=None),
    )

    result = strategy.decide(request)

    assert [v.values[0] for v in result.values] == [4.0, 4.0, 4.0]
    assert result.quantile_level == 5.0
    assert isinstance(result.value_definition, ScalarDefinition)
    assert strategy.name == "simple_conservative"


def test_simple_conservative_requires_production_forecast():
    strategy = SimpleConservativeDayAheadSalesStrategy()

    from app.decisions.request import (
        DayAheadSalesDecisionRequest,
        DeliveryWindow as Window,
    )

    tz = dt.timezone.utc
    request = DayAheadSalesDecisionRequest(
        portfolio_id=7,
        delivery_window=Window(dt.datetime(2026, 6, 2, 0, 0, tzinfo=tz),
                               dt.datetime(2026, 6, 2, 1, 0, tzinfo=tz)),
    )

    try:
        strategy.decide(request)
    except ValueError:
        return
    raise AssertionError("missing production forecast should fail the strategy")
