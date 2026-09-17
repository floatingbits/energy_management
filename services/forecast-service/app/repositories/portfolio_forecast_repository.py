from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.forecasting.enums import ForecastMetric
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.encoding.serializers import serialize
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.models import TimeSeriesGroup as TimeSeriesGroupModel, TimeSeriesTimeBase as TimeSeriesTimeBaseModel, TimeSeries as TimeSeriesModel, TimeSeriesValue as TimeSeriesValueModel
from app.portfolio_forecast.models import PortfolioForecast as PortfolioForecastModel


class PortfolioForecastRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(
        self,
        portfolio_id: int,
        time_series_time_base: TimeSeriesTimeBase,
        series: TimeSeries,
        aggregation_model: str,
        based_on_revision: int,
    ):

        run = TimeSeriesTimeBaseModel(
            start=time_series_time_base.start,
            resolution_seconds=time_series_time_base.resolution.total_seconds(),
            slots=time_series_time_base.slots,
        )

        self.db_session.add(run)

        self.db_session.flush()

        time_series_group = TimeSeriesGroupModel(
            time_series_time_base_id=run.id
        )

        self.db_session.add(time_series_group)

        self.db_session.flush()

        portfolio_forecast = PortfolioForecastModel(
            portfolio_id=portfolio_id,
            forecast_id=time_series_group.id,
            aggregation_model=aggregation_model,
            based_on_revision=based_on_revision,
            created_at=datetime.now(timezone.utc),
        )

        self.db_session.add(portfolio_forecast)

        self.db_session.flush()

        db_series = TimeSeriesModel(
            time_series_group_id=time_series_group.id,
            metric=series.metric,
            value_type_definition=series.value_definition.serialize(),
        )

        self.db_session.add(db_series)

        self.db_session.flush()

        for index, value in enumerate(series.values):
            self.db_session.add(
                TimeSeriesValueModel(
                    time_series_id=db_series.id,
                    slot_index=index,
                    payload=serialize(value, series_definition),
                )
            )

        self.db_session.commit()

        return portfolio_forecast

    def get_latest_portfolio_forecast(
            self,
            portfolio_id: int,
    ) -> PortfolioForecastModel | None:
        stmt = (
            select(PortfolioForecastModel)
            .options(
                selectinload(PortfolioForecastModel.forecast)
                .selectinload(TimeSeriesGroupModel.time_series)
                .selectinload(TimeSeriesModel.values),

                selectinload(PortfolioForecastModel.forecast)
                .selectinload(TimeSeriesGroupModel.time_series_time_base),
            )
            .where(
                PortfolioForecastModel.portfolio_id == portfolio_id
            )
            .join(
                PortfolioForecastModel.forecast
            )
            .join(
                TimeSeriesGroupModel.time_series_time_base
            )
            .order_by(
                TimeSeriesTimeBaseModel.created_at.desc()
            )
            .limit(1)
        )

        return self.db_session.scalar(stmt)
