from sqlalchemy.orm import Session

from app.energy.observation.models import (
    EnergyMarketObservation as EnergyMarketObservationModel,
)
from app.energy.observation.observation import EnergyObservation
from app.forecasting.encoding.definitions import ScalarDefinition
from app.forecasting.encoding.serializers import serialize
from app.forecasting.models import (
    TimeSeriesGroup as TimeSeriesGroupModel,
    TimeSeriesTimeBase as TimeSeriesTimeBaseModel,
    TimeSeries as TimeSeriesModel,
    TimeSeriesValue as TimeSeriesValueModel,
)


class EnergyObservationRepository:
    """Persists EnergyObservations through the generic TimeSeries models.

    Observations are scalar by definition: only series with a
    ScalarDefinition are accepted, so each payload holds one value.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(
        self,
        observation: EnergyObservation,
    ) -> EnergyMarketObservationModel:

        run = TimeSeriesTimeBaseModel(
            start=observation.run.start,
            resolution_seconds=observation.run.resolution.total_seconds(),
            slots=observation.run.slots,
        )

        self.db_session.add(run)
        self.db_session.flush()

        time_series_group = TimeSeriesGroupModel(
            time_series_time_base_id=run.id,
        )

        self.db_session.add(time_series_group)
        self.db_session.flush()

        for series in observation.time_series:
            if not isinstance(series.value_definition, ScalarDefinition):
                raise ValueError(
                    f"Energy observations must be stored as scalar values,"
                    f" but series {series.metric} has a"
                    f" {series.value_definition} definition"
                )

            db_series = TimeSeriesModel(
                time_series_group_id=time_series_group.id,
                metric=series.metric,
                value_type_definition=series.value_definition.serialize(),
            )

            self.db_session.add(db_series)
            self.db_session.flush()

            for index, value in enumerate(series.values):
                self.db_session.add(
                    TimeSeriesValueModel(
                        time_series_id=db_series.id,
                        slot_index=index,
                        payload=serialize(value, series.value_definition),
                    )
                )

        db_observation = EnergyMarketObservationModel(
            time_series_group_id=time_series_group.id,
            location_key=observation.location_key,
            source=observation.provider,
        )

        self.db_session.add(db_observation)

        self.db_session.commit()

        return db_observation
