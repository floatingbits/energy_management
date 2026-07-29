from datetime import timedelta

from app.weather.adapter import WeatherAdapter
from app.weather.provider_result import ProviderForecastResult
from app.weather.request import WeatherForecastRequest
from app.weather.result import (
    WeatherForecastResult,
    WeatherLocationForecast
)

from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_value import ForecastValue
from app.forecasting.domain.metric import ForecastMetric
from app.forecasting.domain.forecast_run import ForecastRun


class DefaultWeatherAdapter(WeatherAdapter):


    def adapt(
        self,
        provider_result: ProviderForecastResult,
        request: WeatherForecastRequest
    ) -> WeatherForecastResult:

        forecasts = []

        for location_forecast in provider_result.forecasts:

            series = []

            for provider_series in location_forecast.series:

                metric = self.map_metric(
                    provider_series.variable_name
                )

                series.append(
                    ForecastSeries(
                        metric=metric,
                        values=[
                            ForecastValue(
                                p50=value
                            )
                            for value in provider_series.values
                        ]
                    )
                )


            forecasts.append(
                WeatherLocationForecast(
                    location=next(
                        location
                        for location in request.locations
                        if (
                            location.latitude
                            == location_forecast.latitude
                            and
                            location.longitude
                            == location_forecast.longitude
                        )
                    ),
                    run=self.create_run(
                        provider_result,
                        location_forecast
                    ),
                    series=series
                )
            )


        return WeatherForecastResult(
            provider=provider_result.provider,
            model=provider_result.model,
            forecasts=forecasts
        )


    def create_run(
        self,
        provider_result,
        location_forecast
    ) -> ForecastRun:

        # vorerst:
        # nimmt erstes Raster an

        first_series = (
            location_forecast.series[0]
        )

        return ForecastRun(
            start=first_series.start,
            resolution=first_series.resolution,
            slots=len(first_series.values)
        )


    def map_metric(
        self,
        variable: str
    ) -> ForecastMetric:

        mapping = {
            "temperature_2m":
                ForecastMetric.TEMPERATURE,

            "wind_speed_10m":
                ForecastMetric.WIND_SPEED,

            "cloud_cover":
                ForecastMetric.CLOUD_COVER,
        }

        return mapping[variable]