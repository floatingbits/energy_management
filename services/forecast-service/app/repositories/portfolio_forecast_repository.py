from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.forecasting.enums import ForecastMetric
from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_run import ForecastRun
from app.forecasting.models import Forecast as ForecastModel, ForecastRun as ForecastRunModel, ForecastSeries as ForecastSeriesModel, ForecastValue as ForecastValueModel
from app.portfolio_forecast.models import PortfolioForecast as PortfolioForecastModel


class PortfolioForecastRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(
        self,
        portfolio_id: int,
        forecast_run: ForecastRun,
        series: ForecastSeries,
        aggregation_model: str,
        based_on_revision: int,
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

        portfolio_forecast = PortfolioForecastModel(
            portfolio_id=portfolio_id,
            forecast_id=forecast.id,
            aggregation_model=aggregation_model,
            based_on_revision=based_on_revision,
            created_at=datetime.now(timezone.utc),
        )

        self.db_session.add(portfolio_forecast)

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

        return portfolio_forecast

    def get_latest_portfolio_forecast(
            self,
            portfolio_id: int,
    ) -> PortfolioForecastModel | None:
        stmt = (
            select(PortfolioForecastModel)
            .options(
                selectinload(PortfolioForecastModel.forecast)
                .selectinload(ForecastModel.series)
                .selectinload(ForecastSeriesModel.values),

                selectinload(PortfolioForecastModel.forecast)
                .selectinload(ForecastModel.forecast_run),
            )
            .where(
                PortfolioForecastModel.portfolio_id == portfolio_id
            )
            .join(
                PortfolioForecastModel.forecast
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
