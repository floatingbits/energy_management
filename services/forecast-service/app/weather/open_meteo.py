from app.weather.provider import WeatherProvider
from app.weather.value_objects import WeatherLocation


class OpenMeteoProvider(WeatherProvider):



    def get_forecast(
        self,
        locations: list[WeatherLocation],
        horizon_start,
        horizon_end,
        resolution_minutes,
    ):

        raise NotImplementedError