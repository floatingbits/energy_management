from argparse import ArgumentParser
from datetime import datetime, timezone

from app.bootstrap.energy_observation import (
    create_energy_observation_service,
)
from app.energy.observation.service import EnergyObservationService


class FetchEnergyObservationsJob:

    def __init__(
        self,
        service: EnergyObservationService,
    ):
        self.service = service

    def run(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ):
        return self.service.fetch_observations(
            start=start,
            end=end,
        )


def main():
    parser = ArgumentParser(
        description="Fetch and store energy market observations",
    )
    parser.add_argument(
        "--start",
        type=datetime.fromisoformat,
        default=None,
    )
    parser.add_argument(
        "--end",
        type=datetime.fromisoformat,
        default=None,
    )
    arguments = parser.parse_args()

    service = create_energy_observation_service()
    job = FetchEnergyObservationsJob(service)

    observations = job.run(
        start=arguments.start,
        end=arguments.end,
    )

    print(
        f"Stored {len(observations)} energy market observation(s)"
    )


if __name__ == "__main__":
    main()
