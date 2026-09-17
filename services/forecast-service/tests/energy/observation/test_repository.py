from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import app.forecasting.models  # noqa: F401 - register forecasting tables
import app.energy.observation.models  # noqa: F401 - register observation table
from app.database import Base
from app.energy.observation.observation import EnergyObservation
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series_value import TimeSeriesValue
from app.forecasting.encoding.definitions import (
    DEFAULT_QUANTILE_DEFINITION,
    ScalarDefinition,
)
from app.forecasting.enums import ForecastMetric
from app.forecasting.models import (
    TimeSeries as TimeSeriesModel,
    TimeSeriesValue as TimeSeriesValueModel,
)
from app.repositories.energy_observation_repository import (
    EnergyObservationRepository,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


def scalar_observation() -> EnergyObservation:
    return EnergyObservation(
        location_key="DE",
        provider="SMARD",
        run=TimeSeriesTimeBase(
            start=datetime(2024, 12, 4, 9, 40, tzinfo=timezone.utc),
            resolution=timedelta(minutes=15),
            slots=3,
        ),
        time_series=[
            TimeSeries(
                metric=ForecastMetric.TOTAL_ENERGY_CONSUMPTION,
                values=[
                    TimeSeriesValue((1.0,)),
                    TimeSeriesValue((None,)),
                    TimeSeriesValue((3.0,)),
                ],
                value_definition=ScalarDefinition(),
            ),
            TimeSeries(
                metric=ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE,
                values=[
                    TimeSeriesValue((10.5,)),
                    TimeSeriesValue((11.5,)),
                    TimeSeriesValue((12.5,)),
                ],
                value_definition=ScalarDefinition(),
            ),
        ],
    )


def test_save_persists_scalar_observation(session):
    repository = EnergyObservationRepository(session)

    observation = repository.save(scalar_observation())

    assert observation.location_key == "DE"
    assert observation.source == "SMARD"
    assert observation.created_at is not None

    series = list(session.scalars(
        select(TimeSeriesModel)
        .where(TimeSeriesModel.time_series_group_id
               == observation.time_series_group_id)
    ))
    assert {s.metric for s in series} == {
        "total_energy_consumption",
        "day_ahead_electricity_price",
    }
    for series_row in series:
        assert series_row.value_type_definition == '{"type": "scalar"}'

    payloads = session.scalars(
        select(TimeSeriesValueModel.payload)
        .where(TimeSeriesValueModel.time_series_id == series[0].id)
        .order_by(TimeSeriesValueModel.slot_index)
    ).all()
    assert payloads == ["[1.0]", "[null]", "[3.0]"]


def test_save_rejects_quantile_series(session):
    repository = EnergyObservationRepository(session)
    observation = scalar_observation()
    from app.forecasting.domain.time_series_value import from_quantiles
    quantile_series = TimeSeries(
        metric=ForecastMetric.TOTAL_ENERGY_CONSUMPTION,
        values=[from_quantiles(p05=1, p50=2, p95=3)],
        value_definition=DEFAULT_QUANTILE_DEFINITION,
    )

    import dataclasses
    observation = dataclasses.replace(
        observation,
        time_series=[quantile_series],
    )

    with pytest.raises(ValueError, match="scalar"):
        repository.save(observation)
    session.rollback()


def test_save_two_observations_get_distinct_groups(session):
    repository = EnergyObservationRepository(session)

    first = repository.save(scalar_observation())
    second = repository.save(scalar_observation())

    assert first.id != second.id
    assert first.time_series_group_id != second.time_series_group_id
