from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

import app.forecasting.models  # noqa: F401 - register forecasting tables
import app.energy.market_forecast.models  # noqa: F401 - register price forecast table
from app.database import Base, get_db
from app.energy.market_forecast.core.domain import EnergyMarketForecast
from app.energy.market_forecast.router import router
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series_value import TimeSeriesValue
from app.forecasting.encoding.definitions import ScalarDefinition
from app.forecasting.enums import ForecastMetric
from app.repositories.energy_market_forecast_repository import (
    EnergyMarketForecastRepository,
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


def market_forecast() -> EnergyMarketForecast:
    return EnergyMarketForecast(
        market="DE-LU",
        provider="sarimax",
        run=TimeSeriesTimeBase(
            start=datetime(2024, 12, 4, 9, 40, tzinfo=timezone.utc),
            resolution=timedelta(minutes=15),
            slots=2,
        ),
        time_series=[
            TimeSeries(
                metric=ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE,
                values=[
                    TimeSeriesValue((10.5,)),
                    TimeSeriesValue((11.5,)),
                ],
                value_definition=ScalarDefinition(),
            ),
        ],
    )


def test_get_market_forecasts_returns_stored_forecasts(db_session, client):
    repository = EnergyMarketForecastRepository(db_session)

    repository.save(market_forecast())

    response = client.get("/energy-market-forecasts/")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["market"] == "DE-LU"
    assert body[0]["source"] == "sarimax"

    group = body[0]["forecast"]
    assert group["time_series_time_base"]["slots"] == 2

    series = group["time_series"][0]
    assert series["metric"] == "day_ahead_electricity_price"
    assert [value["values"] for value in series["values"]] == [
        [10.5], [11.5],
    ]


def test_get_market_forecast_by_unknown_id_returns_404(client):
    response = client.get("/energy-market-forecasts/999")

    assert response.status_code == 404
