from datetime import timedelta

from app.weather.models.weather_forecast import WeatherForecast as WeatherForecastModel

from app.weather.result import (
    WeatherLocationForecast,
    WeatherLocation,
)

from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_value import TimeSeriesValue
from app.forecasting.encoding.definitions import definition_from_payload
from app.forecasting.encoding.serializers import parser_for


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

            definition = definition_from_payload(db_series.value_type_definition)
            parser = parser_for(definition)

            series.append(
                TimeSeries(
                    metric=db_series.metric,
                    value_definition=definition,
                    values=[parser.parse(value.payload) for value in db_series.values],
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
