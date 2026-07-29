from datetime import timezone, datetime, timedelta

from app.weather.provider import WeatherProvider
from app.weather.provider_result import ProviderForecastResult, ProviderSeries, ProviderLocationForecast
from app.weather.request import WeatherForecastRequest



class FakeWeatherProvider(WeatherProvider):

    def get_forecast(
            self,
            request: WeatherForecastRequest
    ) -> ProviderForecastResult:

        series = [
            ProviderSeries(
                variable_name="temperature_2m",
                start=datetime.now(timezone.utc),
                resolution=timedelta(hours=1),
                values=[1.]
            )
        ]
        forecasts = [
            ProviderLocationForecast(
                longitude=request.locations[0].longitude,
                latitude=request.locations[0].latitude,
                series=series,
            )
        ]

        return ProviderForecastResult(
            provider="fake",
            model='unknown',
            forecasts=forecasts
        )