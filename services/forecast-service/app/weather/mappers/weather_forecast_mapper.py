from datetime import timedelta

from app.weather.models.weather_forecast import WeatherForecast as WeatherForecastModel

from app.weather.result import (
    WeatherLocationForecast,
    WeatherLocation,
)

from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_value import TimeSeriesValue


class WeatherForecastMapper:

    def to_domain(
        self,
        model: WeatherForecastModel,
    ) -> WeatherLocationForecast:

        run = TimeSeriesTimeBase(
            start=model.forecast.time_series_time_base.start,
            resolution=timedelta(seconds=model.forecast.time_series_time_base.resolution_seconds),
            slots=model.forecast.time_series_time_base.slots,
        )


        series = []

        for db_series in model.forecast.time_series:

            series.append(
                TimeSeries(
                    metric=db_series.metric,
                    values=[
                        TimeSeriesValue(
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