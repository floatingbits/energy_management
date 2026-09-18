from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.energy.observation.schemas import (
    EnergyMarketObservationResponse,
)
from app.repositories.energy_observation_repository import (
    EnergyObservationRepository,
)

router = APIRouter(
    prefix="/energy-market-observations",
    tags=["Energy Market Observations"],
)


@router.get(
    "/",
    response_model=list[EnergyMarketObservationResponse],
)
def get_energy_market_observations(
    location_key: str | None = None,
    db: Session = Depends(get_db),
):

    repository = EnergyObservationRepository(db)

    return repository.get_observations(location_key)


@router.get(
    "/{observation_id}",
    response_model=EnergyMarketObservationResponse,
)
def get_energy_market_observation(
    observation_id: int,
    db: Session = Depends(get_db),
):

    repository = EnergyObservationRepository(db)

    observation = repository.get_observation(observation_id)

    if observation is None:
        raise HTTPException(
            status_code=404,
            detail="Energy Market Observation not found",
        )

    return observation
