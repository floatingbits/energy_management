from app.asset_forecast.service import AssetForecastService
from app.services.asset_forecast_requirement_service import AssetForecastRequirementService

from app.weather.location import WeatherLocation



class ProcessRequiredForecasts:
    def __init__(
        self,
        requirement_service: AssetForecastRequirementService,
        asset_service,
        weather_forecast_requirement_service,
        asset_forecast_checker,
        asset_forecast_service,
    ):
        self.requirement_service = requirement_service
        self.asset_service = asset_service
        self.weather_forecast_requirement_service = weather_forecast_requirement_service
        self.asset_forecast_checker = asset_forecast_checker
        self.asset_forecast_service = asset_forecast_service

    def execute(self) -> None:
        # 1. Welche Assets sind grundsätzlich forecast-relevant?
        requirements = self.requirement_service.get_all()

        required_asset_ids = {
            requirement.asset_id
            for requirement in requirements
        }

        # 2. Alle bekannten Assets auf WeatherLocations abbilden.
        #
        # Ergebnis z.B.:
        #
        # {
        #     WeatherLocation(...): [17, 23],
        #     WeatherLocation(...): [42],
        # }
        #
        locations, asset_locations = self.asset_service.get_weather_locations()

        # 3. Für tatsächlich relevante Locations einen aktuellen
        #    WeatherForecast sicherstellen.
        weather_forecast_ids = []

        for location, asset_ids in locations.items():

            # Location hat zwar Assets, aber keines davon hat
            # aktuell ein ForecastRequirement.
            if not any(
                asset_id in required_asset_ids
                for asset_id in asset_ids
            ):
                continue


            weather_forecast_ids[location] = (
                self.weather_forecast_requirement_service.get_or_create_suitable(location)
            )

        # 4. AssetForecasts prüfen/erzeugen.
        affected_asset_ids = []

        for requirement in requirements:
            location = asset_locations[requirement.asset_id]
            weather_forecast_id = weather_forecast_ids[location]
            result = self.asset_forecast_checker.check(
                requirement=requirement,
                weather_forecast_id=weather_forecast_id,
            )

            if not result.required:
                continue

            self.asset_forecast_service.generate(
                asset_id=requirement.asset_id,
                weather_forecast_id=weather_forecast_id,
            )

            affected_asset_ids.append(requirement.asset_id)

        # 5. Später:
        #    Aus affected_asset_ids betroffene Portfolios bestimmen
        #    und PortfolioForecasts aggregieren.