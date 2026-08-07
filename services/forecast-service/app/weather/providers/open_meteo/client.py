import openmeteo_requests

import requests_cache
from retry_requests import retry


class Client:
    API_URL_CURRENT_FORECAST = "https://api.open-meteo.com/v1/forecast"
    def __init__(self, api_url=None):
        self.api_url = api_url if api_url is not None else self.API_URL_CURRENT_FORECAST

    def get_current_forecast(self, params:dict) -> list:
        openmeteo = self.build_openmeteo_client()
        return openmeteo.weather_api(self.api_url, params = params)

    def build_openmeteo_client(self):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        return openmeteo_requests.Client(session=retry_session)