from argparse import ArgumentParser
from datetime import timedelta

from app.bootstrap.energy_market_forecast import (
    create_energy_market_forecast_service,
)
from app.forecasting.enums import ForecastMetric


class GenerateEnergyMarketForecastJob:

    def __init__(self, service):
        self.service = service

    def run(self, market: str, hours: int, variable: ForecastMetric):
        return self.service.generate(
            market=market,
            horizon=timedelta(hours=hours),
            variable=variable,
        )


def main():
    parser = ArgumentParser(
        description="Generate and store an energy market forecast",
    )
    parser.add_argument(
        "--market",
        type=str,
        default="DE-LU",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
    )
    parser.add_argument(
        "--variable",
        type=str,
        default=str(ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE),
    )
    arguments = parser.parse_args()

    service = create_energy_market_forecast_service()
    job = GenerateEnergyMarketForecastJob(service)

    forecast = job.run(
        market=arguments.market,
        hours=arguments.hours,
        variable=arguments.variable,
    )

    print(
        f"Stored energy market forecast for market {forecast.market} "
        f"and variable {str(forecast.variable)} "
        f"starting at {forecast.run.start.isoformat()} "
        f"covering {forecast.run.slots} slots"
    )


if __name__ == "__main__":
    main()
