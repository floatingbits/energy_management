import requests


class AssetClient:

    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url


    def get_asset(
        self,
        asset_id: int,
    ):

        response = requests.get(
            f"{self.base_url}/assets/{asset_id}"
        )

        response.raise_for_status()

        return response.json()

    def get_assets(
        self
    ):

        response = requests.get(
            f"{self.base_url}/assets"
        )

        response.raise_for_status()

        return response.json()