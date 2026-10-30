"""Persistence of day-ahead sales decisions in the well known manner."""

from em_timeseries.encoding import serialize

from app.orm.time_series import (
    TimeSeries,
    TimeSeriesGroup,
    TimeSeriesTimeBase,
    TimeSeriesValue,
)
from app.decisions.models import DayAheadSalesDecision


class DayAheadSalesDecisionRepository:

    def __init__(self, db_session):
        self.db_session = db_session

    def save(
        self,
        request,
        result,
        strategy_name: str,
    ) -> DayAheadSalesDecision:
        """Populate and persist a decision from a strategy result.

        The result's series sits on the delivery window's grid (see the
        alignment module); both are carried by the request.
        """
        window = request.delivery_window
        slots = len(result.values)
        if slots == 0:
            raise ValueError(
                "Strategy result carries no values; nothing to persist"
            )
        window_seconds = window.duration_seconds
        resolution = window_seconds // slots
        if window_seconds % slots:
            raise ValueError(
                f"Result slots ({slots}) do not evenly divide the delivery "
                f"window {window.start}..{window.end}"
            )

        time_base = TimeSeriesTimeBase(
            start=window.start,
            resolution_seconds=resolution,
            slots=slots,
        )
        group = TimeSeriesGroup(
            time_series_time_base=time_base,
        )

        series = TimeSeries(
            metric=result.metric,
            value_type_definition=result.value_definition.serialize(),
            time_series_group=group,
        )

        for slot_index, value in enumerate(result.values):
            series.values.append(
                TimeSeriesValue(
                    slot_index=slot_index,
                    payload=serialize(value, result.value_definition),
                    value_type=value.value_type,
                ),
            )

        decision = DayAheadSalesDecision(
            portfolio_id=request.portfolio_id,
            market=request.market,
            delivery_start=window.start,
            delivery_end=window.end,
            strategy=strategy_name,
            based_on_portfolio_forecast_id=(
                request.production_forecast.forecast_id
                if request.production_forecast else None
            ),
            based_on_price_forecast_id=(
                request.price_forecast.forecast_id
                if request.price_forecast else None
            ),
            quantile_level=result.quantile_level,
            time_series_group=group,
        )

        self.db_session.add(decision)
        self.db_session.commit()
        self.db_session.refresh(decision)

        return decision
