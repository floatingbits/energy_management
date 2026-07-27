from datetime import datetime

from app.schemas.weather import (
    WeatherForecastResult,
    WeatherForecastPoint,
    WeatherVariableValue
)


class FakeWeatherProvider:


    def get_forecast(
        self,
        locations,
        horizon_start,
        horizon_end,
        resolution_minutes
    ):

        return WeatherForecastResult(
            provider="fake",
            model="test",
            forecasts=[
                WeatherForecastPoint(
                    latitude=locations[0].latitude,
                    longitude=locations[0].longitude,
                    period_start=horizon_start,
                    period_end=horizon_end,
                    variables=[
                        WeatherVariableValue(
                            variable="wind_speed",
                            p05=5,
                            p50=10,
                            p95=15
                        )
                    ]
                )
            ]
        )