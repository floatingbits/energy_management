from datetime import datetime

from app.energy.observation.observation import EnergyObservation
from app.energy.observation.provider import EnergyObservationProvider
from app.energy.observation.request import EnergyObservationRequest
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series_value import TimeSeriesValue
from app.forecasting.encoding.definitions import ScalarDefinition
from app.forecasting.enums import ForecastMetric
from app.repositories.energy_observation_repository import (
    EnergyObservationRepository,
)


class EnergyObservationService:
    """Fetches energy market observations from an API provider and stores them.

    Observations are stored as scalar values: every series is built with a
    ScalarDefinition, so each TimeSeriesValue carries exactly one value.
    """

    def __init__(
        self,
        provider: EnergyObservationProvider,
        repository: EnergyObservationRepository,
    ):
        self.provider = provider
        self.repository = repository

    def fetch_latest(self) -> list:
        return self.fetch_observations()

    def fetch_observations(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list:
        """Fetch observations and save them via the repository.

        start=None fetches the latest available series from the provider
        (for SMARD that is the latest series chunk, covering roughly a week).
        When end is given, the slot window is trimmed to it.
        """
        request = EnergyObservationRequest(start=start)
        provider_result = self.provider.get_observations(request)

        observations = []
        for location in provider_result.observations:
            observation = self._to_domain(
                location,
                provider_result.provider,
                end=end,
            )
            observations.append(
                self.repository.save(observation)
            )
        return observations

    @staticmethod
    def _to_domain(location, provider: str, end: datetime | None) -> EnergyObservation:
        first = location.series[0]
        slots = len(first.values)
        if end is not None:
            slots = min(
                slots,
                int(
                    (
                        end - first.start
                    ).total_seconds()
                    // first.resolution.total_seconds()
                ) + 1,
            )

        series_list = [
            TimeSeries(
                metric=ForecastMetric(series.variable_name),
                values=[
                    TimeSeriesValue((value,))
                    for value in series.values[:slots]
                ],
                value_definition=ScalarDefinition(),
            )
            for series in location.series
        ]

        return EnergyObservation(
            location_key=location.location_key,
            provider=provider,
            run=TimeSeriesTimeBase(
                start=first.start,
                resolution=first.resolution,
                slots=slots,
            ),
            time_series=series_list,
        )
