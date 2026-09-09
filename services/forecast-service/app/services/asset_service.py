from collections import defaultdict

from app.weather.location import WeatherLocation


class AssetService:
    def __init__(self, asset_client, weather_service):
        self.asset_client = asset_client
        self.weather_service = weather_service

    def get_weather_locations(self):
        assets = self.asset_client.get_assets()

        asset_coords = [
            (asset["latitude"], asset["longitude"])
            for asset in assets
        ]

        locations = self.weather_service.resolve_locations(asset_coords)

        asset_locations = {}

        for asset, location in zip(assets, locations):
            asset_id = asset["id"]
            asset_locations[asset_id] = location


        return locations, asset_locations