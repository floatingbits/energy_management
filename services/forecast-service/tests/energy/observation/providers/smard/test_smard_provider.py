from datetime import datetime, timezone, timedelta

import pytest
import responses

from app.energy.observation.provider_result import ProviderObservationSeries
from app.energy.observation.providers.smard.client import SmardClient
from app.energy.observation.providers.smard.smard_provider import SmardProvider
from app.energy.observation.request import EnergyObservationRequest
from app.forecasting.enums import ForecastMetric

INDEX_URL = SmardClient.API_URL + "/{filter}/DE/index_quarterhour.json"
SERIES_URL = SmardClient.API_URL + "/{filter}/DE/{filter}_DE_quarterhour_1733305200000.json"

SMARD_INDEX = {"timestamps": [1733305100000, 1733305200000]}
SMARD_CONSUMPTION = {
    "timestamps": [1733305200000 + i * 900000 for i in range(4)],
    "series": [[1733305200000 + i * 900000, 50000.0 + i] for i in range(4)],
}
SMARD_PRICE = {
    "timestamps": [1733305200000 + i * 900000 for i in range(4)],
    "series": [[1733305200000 + i * 900000, 73.5 - i] for i in range(4)],
}


def stub_smard():
    responses.add(responses.GET, INDEX_URL.format(filter="410"), json=SMARD_INDEX, status=200)
    responses.add(responses.GET, SERIES_URL.format(filter="410"), json=SMARD_CONSUMPTION, status=200)
    responses.add(responses.GET, INDEX_URL.format(filter="4169"), json=SMARD_INDEX, status=200)
    responses.add(responses.GET, SERIES_URL.format(filter="4169"), json=SMARD_PRICE, status=200)


@responses.activate
def test_get_observations_returns_series_for_each_variable():
    stub_smard()

    provider = SmardProvider()
    request = EnergyObservationRequest(
        variables=[ForecastMetric.TOTAL_ENERGY_CONSUMPTION, ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE],
    )

    result = provider.get_observations(request)

    assert result.provider == "smard"
    assert len(result.observations) == 1
    assert result.observations[0].location_key == "DE"
    assert len(result.observations[0].series) == 2

    consumption = result.observations[0].series[0]
    price = result.observations[0].series[1]

    assert consumption.variable_name == "total_energy_consumption"
    assert price.variable_name == "day_ahead_electricity_price"

    # scalar values, no quantiles
    assert consumption.values == [50000.0, 50001.0, 50002.0, 50003.0]
    assert price.values == [73.5, 72.5, 71.5, 70.5]

    # quarterhour resolution and series start (timestamps are milliseconds UTC)
    assert consumption.resolution == timedelta(minutes=15)
    assert consumption.start == datetime(2024, 12, 4, 9, 40, tzinfo=timezone.utc)


@responses.activate
def test_get_observations_uses_index_timestamp_earlier_than_or_equal_start():
    stub_smard()

    provider = SmardProvider()
    start = datetime(2024, 12, 4, 9, 40, 5, tzinfo=timezone.utc)
    request = EnergyObservationRequest(
        variables=[ForecastMetric.TOTAL_ENERGY_CONSUMPTION],
        start=start,
    )

    result = provider.get_observations(request)

    series = result.observations[0].series[0]
    assert series.start == datetime(2024, 12, 4, 9, 40, tzinfo=timezone.utc)


def test_get_observations_accepts_region_and_resolution_parameters():
    provider = SmardProvider()

    request = EnergyObservationRequest(
        variables=[ForecastMetric.TOTAL_ENERGY_CONSUMPTION],
        region="DE-LU",
        resolution=timedelta(hours=1),
    )

    assert request.region == "DE-LU"
    assert request.resolution == timedelta(hours=1)
    default_request = EnergyObservationRequest(variables=[ForecastMetric.TOTAL_ENERGY_CONSUMPTION])
    assert default_request.region == "DE"
    assert default_request.resolution == timedelta(minutes=15)


@responses.activate
def test_get_observations_maps_resolution_to_smard_quarterhour():
    stub_smard()

    provider = SmardProvider()
    request = EnergyObservationRequest(
        variables=[ForecastMetric.TOTAL_ENERGY_CONSUMPTION],
        resolution=timedelta(minutes=15),
    )

    provider.get_observations(request)

    index_request = [r for r in responses.calls if "index_quarterhour.json" in r.request.url]
    assert index_request


@responses.activate
def test_get_observations_rejects_unknown_metric():
    provider = SmardProvider()
    request = EnergyObservationRequest(
        variables=[ForecastMetric.TEMPERATURE],
    )

    with pytest.raises(ValueError):
        provider.get_observations(request)


@responses.activate
def test_provider_series_values_may_contain_none():
    """Missing quotations come as null in SMARD series."""
    responses.add(responses.GET, INDEX_URL.format(filter="410"), json=SMARD_INDEX, status=200)
    smard = {
        "timestamps": [1733305200000, 1733306100000],
        "series": [[1733305200000, 50000.0], [1733306100000, None]],
    }
    responses.add(responses.GET, SERIES_URL.format(filter="410"), json=smard, status=200)

    provider = SmardProvider()
    request = EnergyObservationRequest(variables=[ForecastMetric.TOTAL_ENERGY_CONSUMPTION])

    result = provider.get_observations(request)

    series = result.observations[0].series[0]
    assert isinstance(series, ProviderObservationSeries)
    assert series.values == [50000.0, None]
