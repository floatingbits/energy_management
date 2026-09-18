from abc import ABC, abstractmethod

from app.energy.observation.provider_result import ProviderObservationResult
from app.energy.observation.request import EnergyObservationRequest


class EnergyObservationProvider(ABC):

    @abstractmethod
    def get_observations(
        self,
        request: EnergyObservationRequest,
    ) -> ProviderObservationResult:
        raise NotImplementedError
