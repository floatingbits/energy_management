from datetime import datetime, timedelta, timezone

from app.energy.observation.provider import EnergyObservationProvider
from app.energy.observation.provider_result import (
    ProviderLocationObservations,
    ProviderObservationResult,
    ProviderObservationSeries,
)
from app.energy.observation.service import EnergyObservationService
from app.forecasting.encoding.definitions import ScalarDefinition


class FakeEnergyObservationProvider(EnergyObservationProvider):
    """Returns one canned two-variable result, tracking received requests."""

    def __init__(self, result: ProviderObservationResult):
        self.result = result
        self.requests = []

    def get_observations(self, request):
        self.requests.append(request)
        return self.result


class FakeEnergyObservationRepository:

    def __init__(self):
        self.saved = []

    def save(self, observation):
        self.saved.append(observation)
        return observation


def provider_result(total_values, price_values):
    start = datetime(2024, 12, 4, 9, 40, tzinfo=timezone.utc)
    return ProviderObservationResult(
        provider="smard",
        observations=[
            ProviderLocationObservations(
                location_key="DE",
                series=[
                    ProviderObservationSeries(
                        variable_name="total_energy_consumption",
                        start=start,
                        resolution=timedelta(minutes=15),
                        values=total_values,
                    ),
                    ProviderObservationSeries(
                        variable_name="day_ahead_electricity_price",
                        start=start,
                        resolution=timedelta(minutes=15),
                        values=price_values,
                    ),
                ],
            ),
        ],
    )


def test_fetch_latest_builds_scalar_observation():
    provider = FakeEnergyObservationProvider(
        provider_result(
            [1.0, None, 3.0],
            [10.5, 11.5, 12.5],
        ),
    )
    repository = FakeEnergyObservationRepository()
    service = EnergyObservationService(provider, repository)

    observations = service.fetch_latest()

    assert len(observations) == 1
    observation = observations[0]
    assert observation.location_key == "DE"
    assert observation.provider == "smard"
    assert observation.run.start == datetime(
        2024, 12, 4, 9, 40, tzinfo=timezone.utc
    )
    assert observation.run.resolution == timedelta(minutes=15)
    assert observation.run.slots == 3

    [consumption, price] = observation.time_series
    assert consumption.metric == "total_energy_consumption"
    assert isinstance(consumption.value_definition, ScalarDefinition)
    assert [value.values for value in consumption.values] == [
        (1.0,), (None,), (3.0,)
    ]
    assert price.metric == "day_ahead_electricity_price"
    assert [value.values for value in price.values] == [
        (10.5,), (11.5,), (12.5,)
    ]


def test_fetch_latest_passes_no_start_to_provider():
    provider = FakeEnergyObservationProvider(provider_result([], []))
    service = EnergyObservationService(provider, FakeEnergyObservationRepository())

    service.fetch_latest()

    assert provider.requests[0].start is None


def test_fetch_observations_trims_to_end():
    provider = FakeEnergyObservationProvider(
        provider_result(
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
            [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0],
        ),
    )
    service = EnergyObservationService(
        provider,
        FakeEnergyObservationRepository(),
    )
    end = datetime(2024, 12, 4, 11, 25, tzinfo=timezone.utc)

    observations = service.fetch_observations(
        start=provider.result.observations[0].series[0].start,
        end=end,
    )

    observation = observations[0]
    # end - start = 1h45 => 7 slot starts <= end: 09:40 .. 11:25
    assert observation.run.slots == 7
    assert [value.values for value in observation.time_series[0].values] == [
        (float(i),) for i in range(1, 8)
    ]


def test_fetch_observations_end_before_start_trims_to_empty():
    provider = FakeEnergyObservationProvider(
        provider_result([1.0], [2.0]),
    )
    service = EnergyObservationService(
        provider,
        FakeEnergyObservationRepository(),
    )
    start = datetime(2024, 12, 4, 9, 40, tzinfo=timezone.utc)

    observation = service.fetch_observations(
        start=start,
        end=datetime(2024, 12, 4, 9, 30, tzinfo=timezone.utc),
    )[0]

    assert observation.run.slots == 0
    assert observation.time_series[0].values == []
