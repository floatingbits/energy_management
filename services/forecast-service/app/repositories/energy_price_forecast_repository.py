from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.energy.price_forecast.models import (
    EnergyPriceForecast as EnergyPriceForecastModel,
)
from app.energy.price_forecast.core.domain import EnergyPriceForecast
from app.forecasting.encoding.definitions import ScalarDefinition
from app.forecasting.encoding.serializers import serialize
from app.forecasting.models import (
    TimeSeriesGroup as TimeSeriesGroupModel,
    TimeSeriesTimeBase as TimeSeriesTimeBaseModel,
    TimeSeries as TimeSeriesModel,
    TimeSeriesValue as TimeSeriesValueModel,
)

_EAGER_LOADS = (
    selectinload(EnergyPriceForecastModel.forecast)
    .selectinload(TimeSeriesGroupModel.time_series)
    .selectinload(TimeSeriesModel.values),
    selectinload(EnergyPriceForecastModel.forecast)
    .selectinload(TimeSeriesGroupModel.time_series_time_base),
)


class EnergyPriceForecastRepository:
    """Persists EnergyPriceForecasts through the generic TimeSeries models."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(
        self,
        forecast: EnergyPriceForecast,
    ) -> EnergyPriceForecastModel:
        run = TimeSeriesTimeBaseModel(
            start=forecast.run.start,
            resolution_seconds=forecast.run.resolution.total_seconds(),
            slots=forecast.run.slots,
        )

        self.db_session.add(run)
        self.db_session.flush()

        time_series_group = TimeSeriesGroupModel(
            time_series_time_base_id=run.id,
        )

        self.db_session.add(time_series_group)
        self.db_session.flush()

        for series in forecast.time_series:
            if not isinstance(series.value_definition, ScalarDefinition):
                raise ValueError(
                    f"Price forecasts must be stored as scalar values,"
                    f" but series {series.metric} has a"
                    f" {series.value_definition} definition"
                )

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
                        payload=serialize(value, series.value_definition),
                    )
                )

        db_forecast = EnergyPriceForecastModel(
            time_series_group_id=time_series_group.id,
            market=forecast.market,
            source=forecast.provider,
        )

        self.db_session.add(db_forecast)
        self.db_session.commit()

        return db_forecast

    def get_forecasts(
        self,
        market: str | None = None,
    ) -> list[EnergyPriceForecastModel]:
        stmt = (
            select(EnergyPriceForecastModel)
            .options(*_EAGER_LOADS)
            .order_by(
                EnergyPriceForecastModel.created_at.desc(),
            )
        )

        if market is not None:
            stmt = stmt.where(
                EnergyPriceForecastModel.market == market,
            )

        return list(self.db_session.scalars(stmt))

    def get_forecast(
        self,
        forecast_id: int,
    ) -> EnergyPriceForecastModel | None:
        stmt = (
            select(EnergyPriceForecastModel)
            .options(*_EAGER_LOADS)
            .where(
                EnergyPriceForecastModel.id == forecast_id,
            )
        )

        return self.db_session.scalar(stmt)
