from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_run import ForecastRun
from app.forecasting.models import Forecast as ForecastModel, ForecastRun as ForecastRunModel, ForecastSeries as ForecastSeriesModel, ForecastValue as ForecastValueModel
from app.asset_forecast.models import AssetForecast as AssetForecastModel

class AssetForecastRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(
        self,
        asset_id: int,
        forecast_run: ForecastRun,
        series: ForecastSeries
    ):

        run = ForecastRunModel(
            start=forecast_run.start,
            resolution_seconds=forecast_run.resolution.total_seconds(),
            slots=forecast_run.slots,
        )



        self.db_session.add(run)

        self.db_session.flush()
        forecast = ForecastModel(
            forecast_run_id=run.id
        )

        self.db_session.add(forecast)

        self.db_session.flush()


        asset_forecast = AssetForecastModel(
            asset_id=asset_id,
            forecast_id=forecast.id,
            model="default"
        )

        self.db_session.add(asset_forecast)

        self.db_session.flush()

        db_series = ForecastSeriesModel(
            forecast_id=forecast.id,
            metric=series.metric,
        )

        self.db_session.add(db_series)

        self.db_session.flush()

        for index, value in enumerate(series.values):
            self.db_session.add(
                ForecastValueModel(
                    series_id=db_series.id,
                    slot_index=index,
                    p05=value.p05,
                    p50=value.p50,
                    p95=value.p95,
                )
            )

        self.db_session.commit()

        return forecast

    def get_latest_asset_forecast(
            self,
            asset_id: int,
    ) -> AssetForecastModel | None:
        stmt = (
            select(AssetForecastModel)
            .options(
                selectinload(AssetForecastModel.forecast)
                .selectinload(ForecastModel.series)
                .selectinload(ForecastSeriesModel.values),

                selectinload(AssetForecastModel.forecast)
                .selectinload(ForecastModel.forecast_run),
            )
            .where(
                AssetForecastModel.asset_id == asset_id
            )
            .join(
                AssetForecastModel.forecast
            )
            .join(
                ForecastModel.forecast_run
            )
            .order_by(
                ForecastRunModel.created_at.desc()
            )
            .limit(1)
        )

        return self.db_session.scalar(stmt)

