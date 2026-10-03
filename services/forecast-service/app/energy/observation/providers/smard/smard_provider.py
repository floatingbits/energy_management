from datetime import datetime, timedelta, timezone

from app.energy.observation.provider import EnergyObservationProvider
from app.energy.observation.provider_result import (
    ProviderLocationObservations,
    ProviderObservationResult,
    ProviderObservationSeries,
)
from app.energy.observation.request import EnergyObservationRequest
from app.energy.observation.providers.smard.client import SmardClient
from app.energy.observation.resolutions import SMARD_RESOLUTIONS
from app.forecasting.enums import ForecastMetric

# SMARD filter ids: 410 is the documented "total grid load" consumption
# variable, 4169 the (undocumented) industry wholesale price.
SMARD_FILTERS: dict[ForecastMetric, str] = {
    ForecastMetric.TOTAL_ENERGY_CONSUMPTION: "410",
    ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE: "4169",
}


class SmardProvider(EnergyObservationProvider):

    def __init__(self, client=None):
        if client is None:
            client = SmardClient()
        self.client = client

    def get_observations(
        self,
        request: EnergyObservationRequest,
    ) -> ProviderObservationResult:
        filters = {}
        requested = request.variables or list(SMARD_FILTERS)
        for variable in requested:
            if variable not in SMARD_FILTERS:
                raise ValueError(
                    f"No SMARD filter known for variable {variable}, available: {list(SMARD_FILTERS)}"
                )
            filters[variable] = SMARD_FILTERS[variable]
        resolution = self.smard_resolution(request.resolution)
        series = [
            self.fetch_series(filters[variable], variable, request, resolution)
            for variable in requested
        ]
        observations = [
            ProviderLocationObservations(location_key=request.region, series=series)
        ]
        return ProviderObservationResult(provider="smard", observations=observations)

    def fetch_series(
        self,
        filter_id: str,
        variable: ForecastMetric,
        request: EnergyObservationRequest,
        resolution: str,
    ) -> ProviderObservationSeries:
        index = self.client.get_index(filter_id, request.region, resolution)
        if request.start is None:
            return self.fetch_latest_series(index, filter_id, variable, request, resolution)
        return self.fetch_window_series(index, filter_id, variable, request, resolution)

    def fetch_latest_series(
        self,
        index: list[int],
        filter_id: str,
        variable: ForecastMetric,
        request: EnergyObservationRequest,
        resolution: str,
    ) -> ProviderObservationSeries:
        timestamp = index[-1]
        raw = self.client.get_timeseries(filter_id, request.region, resolution, timestamp)
        values = [value for _, value in raw]
        return ProviderObservationSeries(
            variable_name=str(variable),
            start=datetime.fromtimestamp(timestamp / 1000, timezone.utc),
            resolution=SMARD_RESOLUTIONS[resolution],
            values=values,
        )

    def fetch_window_series(
        self,
        index: list[int],
        filter_id: str,
        variable: ForecastMetric,
        request: EnergyObservationRequest,
        resolution: str,
    ) -> ProviderObservationSeries:
        """Fetch and concatenate all SMARD series chunks covering the
        requested window.

        SMARD serves each series in fixed chunks; all chunks from the last
        one starting at or before the requested start up to (exclusive) the
        requested end are fetched. Values before start and after end are
        not trimmed — the readers align on their grid. Without an end
        only the chunk covering the start is fetched.
        """
        if request.start is None:
            raise ValueError(
                "A start must be given to fetch a window; None fetches the latest series"
            )
        start_ms = int(request.start.timestamp() * 1000)
        end_ms = (
            int(request.end.timestamp() * 1000)
            if request.end is not None
            else None
        )
        candidates = [ts for ts in index if ts <= start_ms]
        if not candidates:
            raise ValueError(
                f"No SMARD series start at or before {request.start.isoformat()}"
            )
        first = candidates[-1]
        timestamps = [
            ts for ts in index
            if first <= ts and (end_ms is None or ts < end_ms)
        ]
        if not timestamps:
            timestamps = [first]
        values = []
        for timestamp in timestamps:
            raw = self.client.get_timeseries(
                filter_id, request.region, resolution, timestamp,
            )
            values.extend(value for _, value in raw)
        return ProviderObservationSeries(
            variable_name=str(variable),
            start=datetime.fromtimestamp(timestamps[0] / 1000, timezone.utc),
            resolution=SMARD_RESOLUTIONS[resolution],
            values=values,
        )

    def smard_resolution(self, resolution: timedelta) -> str:
        for name, res in SMARD_RESOLUTIONS.items():
            if res == resolution:
                return name
        raise ValueError(
            f"Resolution {resolution} is not available in SMARD, choose one of {list(SMARD_RESOLUTIONS)}"
        )
