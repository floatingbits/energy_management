from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.encoding.serializers import serialize
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.models import TimeSeriesGroup as TimeSeriesGroupModel, TimeSeriesTimeBase as TimeSeriesTimeBaseModel, TimeSeries as TimeSeriesModel, TimeSeriesValue as TimeSeriesValueModel
from app.asset_forecast.models import AssetForecast as AssetForecastModel

class AssetForecastRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(
        self,
        asset_id: int,
        time_series_time_base: TimeSeriesTimeBase,
        series: TimeSeries,
        revision: int,
        based_on_weather_forecast_id: int
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


        asset_forecast = AssetForecastModel(
            asset_id=asset_id,
            forecast_id=time_series_group.id,
            model="default",
            based_on_revision=revision,
            based_on_weather_forecast_id=based_on_weather_forecast_id
        )

        self.db_session.add(asset_forecast)

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
                    payload=serialize(value, series.value_definition),
                )
            )

        self.db_session.commit()

        return time_series_group

    def get_latest_asset_forecast(
            self,
            asset_id: int,
    ) -> AssetForecastModel | None:
        stmt = (
            select(AssetForecastModel)
            .options(
                selectinload(AssetForecastModel.forecast)
                .selectinload(TimeSeriesGroupModel.time_series)
                .selectinload(TimeSeriesModel.values),

                selectinload(AssetForecastModel.forecast)
                .selectinload(TimeSeriesGroupModel.time_series_time_base),
            )
            .where(
                AssetForecastModel.asset_id == asset_id
            )
            .join(
                AssetForecastModel.forecast
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

    def get_for_requirements(
        self,
        asset_id: int,
        required_revision: int,
        weather_forecast_id: int,
    ):
        return (
            self.db_session.query(AssetForecastModel)
            .filter(
                AssetForecastModel.asset_id == asset_id,
                AssetForecastModel.based_on_revision >= required_revision,
                AssetForecastModel.based_on_weather_forecast_id == weather_forecast_id,
            )
            .first()
        )