from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

import app.forecasting.models  # noqa: F401 - register forecasting tables
import app.energy.price_forecast.models  # noqa: F401 - register price forecast table
from app.database import Base
from app.energy.price_forecast.core.domain import EnergyPriceForecast
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series_value import TimeSeriesValue
from app.forecasting.encoding.definitions import ScalarDefinition
from app.forecasting.enums import ForecastMetric
from app.forecasting.models import (
    TimeSeries as TimeSeriesModel,
    TimeSeriesValue as TimeSeriesValueModel,
)
from app.repositories.energy_price_forecast_repository import (
    EnergyPriceForecastRepository,
)


@pytest.fixture
def session() -> Session:
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


def price_forecast() -> EnergyPriceForecast:
    return EnergyPriceForecast(
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


def test_save_persists_scalar_forecast(session):
    repository = EnergyPriceForecastRepository(session)

    forecast = repository.save(price_forecast())

    assert forecast.market == "DE-LU"
    assert forecast.source == "sarimax"
    assert forecast.created_at is not None

    series = list(session.scalars(
        select(TimeSeriesModel)
        .where(TimeSeriesModel.time_series_group_id
               == forecast.time_series_group_id)
    ))
    assert {s.metric for s in series} == {"day_ahead_electricity_price"}
    for series_row in series:
        assert series_row.value_type_definition == '{"type": "scalar"}'

    payloads = session.scalars(
        select(TimeSeriesValueModel.payload)
        .where(TimeSeriesValueModel.time_series_id == series[0].id)
        .order_by(TimeSeriesValueModel.slot_index)
    ).all()
    assert payloads == ["[10.5]", "[11.5]"]


def test_get_forecasts_filters_by_market(session):
    repository = EnergyPriceForecastRepository(session)

    stored = repository.save(price_forecast())

    assert [f.id for f in repository.get_forecasts("DE-LU")] == [stored.id]
    assert repository.get_forecasts("FR") == []
