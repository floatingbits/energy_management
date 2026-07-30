from datetime import datetime, timezone, timedelta
from openmeteo_sdk import Model
from app.weather.open_meteo_mapping import OPEN_METEO_VARIABLES
from app.weather.provider import WeatherProvider

from app.weather.provider_result import ProviderForecastResult, ProviderLocationForecast, ProviderSeries
from app.weather.providers.open_meteo.client import Client
from app.weather.providers.open_meteo.params_builder import ParamsBuilder
from app.weather.request import WeatherForecastRequest

def model_to_name(code):
    """convert Model to name"""
    for name, value in Model.Model.__dict__.items():
        if value == code:
            return name
    return None

class OpenMeteoProvider(WeatherProvider):

    def __init__(self, client=None):
        if client is None:
            client = Client()

        self.client = client

    def get_forecast(
            self,
            request: WeatherForecastRequest
    ) -> ProviderForecastResult:

        # Build request
        request_builder = ParamsBuilder()
        locations = [
            {
                "latitude": location.latitude,
                "longitude": location.longitude,
            } for location in request.locations
        ]
        variables = request.variables
        mapping = OPEN_METEO_VARIABLES
        inv_mapping = {v: k for k, v in mapping.items()}
        open_meteo_variables = [inv_mapping[var] for var in variables ]
        request_params = request_builder.build_request_params(locations, open_meteo_variables)
        api_responses = self.client.get_current_forecast(params=request_params)

        # build appropriate response format from API responses
        forecasts = []
        for response in api_responses:
            lat = response.Latitude()
            lon = response.Longitude()
            print("Response", lat, lon, response.Model())
            minutely_15 = response.Minutely15()
            hourly = response.Hourly()
            daily = response.Daily()
            series = []
            containers = [('minutely_15', minutely_15), ('hourly', hourly), ('daily',daily)]
            for container_id, container in containers:
                print(container_id, container)
                if container is None:
                    continue
                print(container.VariablesLength())
                for i in range(0, container.VariablesLength()):
                    var_name = request_params[container_id][i]

                    series.append(ProviderSeries(
                        variable_name=var_name,
                        start=datetime.fromtimestamp(container.Time(), timezone.utc),
                        resolution=timedelta(seconds=container.Interval()),
                        values=container.Variables(i).ValuesAsNumpy().tolist()
                    ))
            forecast = ProviderLocationForecast(
                latitude=lat, longitude=lon,
                series=series
            )
            forecasts.append(forecast)

        return ProviderForecastResult(
            provider="open_meteo",
            model=model_to_name(api_responses[0].Model()), # only one model per Provider Request
            forecasts=forecasts
        )

