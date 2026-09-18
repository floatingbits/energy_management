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
        timestamp = self.series_start(index, request.start)
        raw = self.client.get_timeseries(filter_id, request.region, resolution, timestamp)
        values = [value for _, value in raw]
        return ProviderObservationSeries(
            variable_name=str(variable),
            start=datetime.fromtimestamp(timestamp / 1000, timezone.utc),
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

    def series_start(self, index: list[int], start: datetime | None) -> int:
        """Return the timeseries start point covering the requested observation window.

        None means the latest available series. Otherwise the latest start point in
        the index that is earlier than or equal to the requested start is used.
        """
        if start is None:
            return index[-1]
        start_ms = int(start.timestamp() * 1000)
        candidates = [ts for ts in index if ts <= start_ms]
        if not candidates:
            raise ValueError(
                f"No SMARD series start at or before {start.isoformat()}"
            )
        return candidates[-1]
