from collections import defaultdict

from app.weather.location import WeatherLocation


class AssetService:
    def __init__(self, asset_client, weather_service):
        self.asset_client = asset_client
        self.weather_service = weather_service

    def get_weather_locations(self) -> tuple[dict[WeatherLocation, list[int]], dict[int, WeatherLocation]] :
        assets = self.asset_client.get_assets()

        asset_coords = [
            (asset["latitude"], asset["longitude"])
            for asset in assets
        ]

        locations = self.weather_service.resolve_locations(asset_coords)

        asset_locations = {}
        location_assets = {}
        for asset, location in zip(assets, locations):
            asset_id = asset["id"]
            asset_locations[asset_id] = location
            if location_assets.get(location) is None:
                location_assets[location] = []
            location_assets[location].append(asset_id)



        return location_assets, asset_locations