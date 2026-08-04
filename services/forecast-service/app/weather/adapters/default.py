from datetime import timedelta

import numpy as np

from app.weather.adapter import WeatherAdapter
from app.weather.provider_result import ProviderForecastResult
from app.weather.request import WeatherForecastRequest
from app.weather.resolver import WeatherLocationResolver
from app.weather.result import (
    WeatherForecastResult,
    WeatherLocationForecast
)

from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_value import ForecastValue
from app.forecasting.enums import ForecastMetric
from app.forecasting.domain.forecast_run import ForecastRun


class DefaultWeatherAdapter(WeatherAdapter):

    def __init__(self, variable_mapping: dict[str, ForecastMetric], location_resolver: WeatherLocationResolver):
        self.variable_mapping = variable_mapping
        self.location_resolver = location_resolver

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
                values = provider_series.values

                if provider_series.resolution != request.resolution:
                    values = self.resample(values, provider_series.resolution/request.resolution)


                series.append(
                    ForecastSeries(
                        metric=metric,
                        values=[
                            ForecastValue(
                                p50=value
                            )
                            for value in values
                        ]
                    )
                )
            # API might respond with slightly different locations, so resolve to requested grid
            forecast_location = self.location_resolver.resolve(location_forecast.latitude, location_forecast.longitude)

            forecasts.append(
                WeatherLocationForecast(
                    location=forecast_location,
                    run=self.create_run(
                        provider_result,
                        location_forecast,
                        request
                    ),
                    series=series
                )
            )

            # Check if location has been requested?
            # next(
            #     location
            #     for location in request.locations
            #     if (
            #             location.latitude
            #             == forecast_location.latitude
            #             and
            #             location.longitude
            #             == forecast_location.longitude
            #     )
            # )


        return WeatherForecastResult(
            provider=provider_result.provider,
            model=provider_result.model,
            forecasts=forecasts
        )

    def resample(self, values: list[float], factor: float):
        # simple interpolation in case we have an hourly variable requested at 15 minute grid
        # TODO: make interpolation flexible via strategy per variable, for example.
       return np.interp(np.arange(0, len(values), 1/factor), np.arange(0, len(values)), values)

    def create_run(
        self,
        provider_result,
        location_forecast,
        request: WeatherForecastRequest
    ) -> ForecastRun:

        # vorerst:
        # nimmt erstes Raster an

        first_series = (
            location_forecast.series[0]
        )

        return ForecastRun(
            start=request.start,
            resolution=request.resolution,
            slots=1 + round((request.end - request.start)/request.resolution)
        )


    def map_metric(
        self,
        variable: str
    ) -> ForecastMetric:

        return self.variable_mapping[variable]