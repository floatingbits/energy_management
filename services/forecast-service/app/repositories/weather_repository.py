from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.forecasting.models.forecast_series import ForecastSeries
from app.forecasting.models.forecast_value import ForecastValue
from app.forecasting.models.forecast_run import ForecastRun
from app.forecasting.models.forecast import Forecast
from app.weather.models import (
    WeatherForecast, WeatherSource,
)

from app.weather.result import WeatherForecastResult





class WeatherRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session
    def get_forecasts_for_location(
        self,
        latitude: float,
        longitude: float,
        limit: Optional[int] = None
    ) -> list[WeatherForecast]:

        stmt = (
            select(WeatherForecast)
            .options(
                joinedload(WeatherForecast.forecast)
                    .joinedload(Forecast.forecast_run),

                joinedload(WeatherForecast.forecast)
                    .joinedload(Forecast.series)
                    .joinedload(ForecastSeries.values),

                joinedload(WeatherForecast.source),
            )
            .where(
                WeatherForecast.latitude == latitude,
                WeatherForecast.longitude == longitude,
            )
            .join(WeatherForecast.forecast)
            .join(Forecast.forecast_run)
            .order_by(ForecastRun.created_at.desc())
        )
        if limit is not None:
            stmt = stmt.limit(limit)

        return list(
            self.db_session.scalars(stmt).unique()
        )

    def create_weather_forecast_run(
            self,
            result: WeatherForecastResult
    ):
        # TODO: Data Structure
        result_run = result.forecasts[0].run
        run = ForecastRun(
            start=result_run.start,
            slots=result_run.slots,
            resolution_seconds=result_run.resolution.total_seconds(),

        )

        self.db_session.add(run)

        self.db_session.flush()

        source = WeatherSource(
            model=result.model,
            provider=result.provider,
            version='0.0.1'
        )
        self.db_session.add(source)

        self.db_session.flush()

        for point in result.forecasts:
            forecast = Forecast(
                forecast_run_id=run.id
            )
            self.db_session.add(forecast)
            self.db_session.flush()

            weather_forecast = WeatherForecast(
                forecast_id=forecast.id,
                latitude=point.location.latitude,
                longitude=point.location.longitude,
                source_id=source.id
            )

            self.db_session.add(weather_forecast)

            self.db_session.flush()

            for series in point.series:

                series_model = ForecastSeries(
                    forecast_id=forecast.id,
                    metric=series.metric,
                )

                self.db_session.add(series_model)
                self.db_session.flush()
                for i, value in enumerate(series.values):
                    value_model = ForecastValue(
                        series_id=series_model.id,
                        slot_index=i,
                        p05=value.p05,
                        p50=value.p50,
                        p95=value.p95
                    )

                    self.db_session.add(value_model)
                    self.db_session.flush()

        self.db_session.commit()

        return run
