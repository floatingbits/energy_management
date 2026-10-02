from argparse import ArgumentParser
from datetime import timedelta

from app.bootstrap.energy_price_forecast import (
    create_energy_price_forecast_service,
)


class GenerateEnergyPriceForecastJob:

    def __init__(self, service):
        self.service = service

    def run(self, market: str, hours: int):
        return self.service.generate(
            market=market,
            horizon=timedelta(hours=hours),
        )


def main():
    parser = ArgumentParser(
        description="Generate and store an energy price forecast",
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
    arguments = parser.parse_args()

    service = create_energy_price_forecast_service()
    job = GenerateEnergyPriceForecastJob(service)

    forecast = job.run(
        market=arguments.market,
        hours=arguments.hours,
    )

    print(
        f"Stored energy price forecast for market {forecast.market} "
        f"starting at {forecast.run.start.isoformat()} "
        f"covering {forecast.run.slots} slots"
    )


if __name__ == "__main__":
    main()
