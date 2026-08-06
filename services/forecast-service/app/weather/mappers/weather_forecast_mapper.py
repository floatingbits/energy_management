from datetime import timedelta

from app.weather.models.weather_forecast import WeatherForecast as WeatherForecastModel

from app.weather.result import (
    WeatherLocationForecast,
    WeatherLocation,
)

from app.forecasting.domain.forecast_run import ForecastRun
from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_value import ForecastValue


class WeatherForecastMapper:

    def to_domain(
        self,
        model: WeatherForecastModel,
    ) -> WeatherLocationForecast:

        run = ForecastRun(
            start=model.forecast.forecast_run.start,
            resolution=timedelta(seconds=model.forecast.forecast_run.resolution_seconds),
            slots=model.forecast.forecast_run.slots,
        )


        series = []

        for db_series in model.forecast.series:

            series.append(
                ForecastSeries(
                    metric=db_series.metric,
                    values=[
                        ForecastValue(
                            p05=value.p05,
                            p50=value.p50,
                            p95=value.p95,
                        )
                        for value in db_series.values
                    ],
                )
            )


        return WeatherLocationForecast(
            location=WeatherLocation(
                latitude=model.latitude,
                longitude=model.longitude,
            ),
            run=run,
            series=series,
        )