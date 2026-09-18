import requests


class SmardClient:

    API_URL = "https://www.smard.de/app/chart_data"

    def __init__(self, api_url=None):
        self.api_url = api_url if api_url is not None else self.API_URL

    def get_index(self, filter_id: str, region: str, resolution: str) -> list[int]:
        """Fetch the index of available timeseries start points, as unix timestamps
        in milliseconds.

        https://www.smard.de/app/chart_data/{filter}/{region}/index_{resolution}.json
        """
        url = f"{self.api_url}/{filter_id}/{region}/index_{resolution}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["timestamps"]

    def get_timeseries(
        self,
        filter_id: str,
        region: str,
        resolution: str,
        timestamp: int,
    ) -> list[list[float | None]]:
        """Fetch a timeseries starting at the given unix timestamp in milliseconds,
        as [timestamp_ms, value] pairs; value may be None for missing quotations.

        https://www.smard.de/app/chart_data/{filter}/{region}/{filter}_{region}_{resolution}_{timestamp}.json
        """
        url = f"{self.api_url}/{filter_id}/{region}/{filter_id}_{region}_{resolution}_{timestamp}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["series"]
