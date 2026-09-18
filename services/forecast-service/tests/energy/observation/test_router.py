from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

import app.forecasting.models  # noqa: F401 - register forecasting tables
import app.energy.observation.models  # noqa: F401 - register observation table
from app.database import Base, get_db
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series_value import TimeSeriesValue
from app.forecasting.encoding.definitions import ScalarDefinition
from app.forecasting.enums import ForecastMetric
from app.energy.observation.observation import EnergyObservation
from app.energy.observation.router import router
from app.repositories.energy_observation_repository import (
    EnergyObservationRepository,
)


@pytest.fixture
def db_session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(db_session: Session) -> TestClient:
    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


def scalar_observation() -> EnergyObservation:
    return EnergyObservation(
        location_key="DE",
        provider="SMARD",
        run=TimeSeriesTimeBase(
            start=datetime(2024, 12, 4, 9, 40, tzinfo=timezone.utc),
            resolution=timedelta(minutes=15),
            slots=2,
        ),
        time_series=[
            TimeSeries(
                metric=ForecastMetric.TOTAL_ENERGY_CONSUMPTION,
                values=[
                    TimeSeriesValue((1.0,)),
                    TimeSeriesValue((2.0,)),
                ],
                value_definition=ScalarDefinition(),
            ),
        ],
    )


def test_get_observations_returns_stored_observations(db_session, client):
    repository = EnergyObservationRepository(db_session)

    repository.save(scalar_observation())
    repository.save(scalar_observation())

    response = client.get("/energy-market-observations/")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["location_key"] == "DE"
    assert body[0]["source"] == "SMARD"

    group = body[0]["observation"]
    assert group["time_series_time_base"]["slots"] == 2
    assert group["time_series_time_base"]["resolution_seconds"] == 900

    series = group["time_series"][0]
    assert series["metric"] == "total_energy_consumption"
    assert series["value_type_definition"] == '{"type": "scalar"}'
    assert [value["values"] for value in series["values"]] == [
        [1.0], [2.0],
    ]


def test_get_observations_filters_by_location_key(db_session, client):
    repository = EnergyObservationRepository(db_session)

    repository.save(scalar_observation())

    response = client.get(
        "/energy-market-observations/?location_key=FR",
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_observation_by_id(db_session, client):
    repository = EnergyObservationRepository(db_session)

    stored = repository.save(scalar_observation())

    response = client.get(f"/energy-market-observations/{stored.id}")

    assert response.status_code == 200
    assert response.json()["id"] == stored.id


def test_get_observation_by_unknown_id_returns_404(client):
    response = client.get("/energy-market-observations/999")

    assert response.status_code == 404
