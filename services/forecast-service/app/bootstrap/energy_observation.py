from app.energy.observation.providers.smard.client import (
    SmardClient,
)
from app.energy.observation.providers.smard.smard_provider import (
    SmardProvider,
)
from app.energy.observation.service import EnergyObservationService
from app.database import SessionLocal
from app.repositories.energy_observation_repository import (
    EnergyObservationRepository,
)


def create_smard_client():
    return SmardClient()


def create_smard_provider():
    return SmardProvider(
        client=create_smard_client(),
    )


def create_energy_observation_repository():
    return EnergyObservationRepository(
        SessionLocal(),
    )


def create_energy_observation_service():
    return EnergyObservationService(
        provider=create_smard_provider(),
        repository=create_energy_observation_repository(),
    )
