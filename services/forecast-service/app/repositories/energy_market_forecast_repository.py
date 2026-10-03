from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.energy.market_forecast.core.domain import EnergyMarketForecast
from app.forecasting.domain.time_series_value import TimeSeriesValue
from app.energy.market_forecast.models import (
    EnergyMarketForecast as EnergyMarketForecastModel,
    EnergyMarketForecastBasis as EnergyMarketForecastBasisModel,
)
from app.forecasting.encoding.definitions import ScalarDefinition
from app.forecasting.encoding.serializers import serialize
from app.forecasting.models import (
    TimeSeriesGroup as TimeSeriesGroupModel,
    TimeSeriesTimeBase as TimeSeriesTimeBaseModel,
    TimeSeries as TimeSeriesModel,
    TimeSeriesValue as TimeSeriesValueModel,
)

_EAGER_LOADS = (
    selectinload(EnergyMarketForecastModel.forecast)
    .selectinload(TimeSeriesGroupModel.time_series)
    .selectinload(TimeSeriesModel.values),
    selectinload(EnergyMarketForecastModel.forecast)
    .selectinload(TimeSeriesGroupModel.time_series_time_base),
    selectinload(EnergyMarketForecastModel.basis)
    .selectinload(EnergyMarketForecastBasisModel.series)
    .selectinload(TimeSeriesModel.values),
    selectinload(EnergyMarketForecastModel.basis)
    .selectinload(EnergyMarketForecastBasisModel.series)
    .selectinload(TimeSeriesModel.time_series_group)
    .selectinload(TimeSeriesGroupModel.time_series_time_base),
)


class EnergyMarketForecastRepository:
    """Persists EnergyMarketForecasts through the generic TimeSeries models."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(
        self,
        forecast: EnergyMarketForecast,
    ) -> EnergyMarketForecastModel:
        run = self._store_run(
            base=forecast.run,
            series=forecast.time_series,
        )

        db_forecast = EnergyMarketForecastModel(
            time_series_group_id=run.id,
            market=forecast.market,
            variable=str(forecast.variable),
            source=forecast.provider,
        )

        self.db_session.add(db_forecast)
        self.db_session.flush()

        for item in forecast.basis:
            group = self._store_run(
                base=item.run.base,
                series=[item.run.series],
            )
            # The run stores exactly one series; the reference is
            # series-level, since the basis is inherently per variable.
            self.db_session.add(
                EnergyMarketForecastBasisModel(
                    energy_market_forecast_id=db_forecast.id,
                    time_series_id=group.time_series[0].id,
                    role=str(item.role),
                    series_name=item.name,
                    metadata_=item.metadata,
                )
            )

        self.db_session.commit()

        return db_forecast

    def _store_run(
        self,
        base,
        series,
    ) -> TimeSeriesGroupModel:
        """Persist a run's time base, group and scalar series."""
        run_model = TimeSeriesTimeBaseModel(
            start=base.start,
            resolution_seconds=base.resolution.total_seconds(),
            slots=base.slots,
        )

        self.db_session.add(run_model)
        self.db_session.flush()

        time_series_group = TimeSeriesGroupModel(
            time_series_time_base_id=run_model.id,
        )

        self.db_session.add(time_series_group)
        self.db_session.flush()

        for item in series:
            if not isinstance(item.value_definition, ScalarDefinition):
                raise ValueError(
                    f"Market forecasts must be stored as scalar values,"
                    f" but series {item.metric} has a"
                    f" {item.value_definition} definition"
                )

            db_series = TimeSeriesModel(
                time_series_group_id=time_series_group.id,
                metric=item.metric,
                value_type_definition=item.value_definition.serialize(),
            )

            self.db_session.add(db_series)
            self.db_session.flush()

            for index, value in enumerate(item.values):
                # Forecast series carry TimeSeriesValue models; basis
                # runs from the providers hold plain scalars.
                model_value = (
                    value
                    if isinstance(value, TimeSeriesValue)
                    else TimeSeriesValue((value,))
                )
                self.db_session.add(
                    TimeSeriesValueModel(
                        time_series_id=db_series.id,
                        slot_index=index,
                        payload=serialize(model_value, item.value_definition),
                    )
                )

        return time_series_group

    def get_forecasts(
        self,
        market: str | None = None,
        variable: str | None = None,
    ) -> list[EnergyMarketForecastModel]:
        stmt = (
            select(EnergyMarketForecastModel)
            .options(*_EAGER_LOADS)
            .order_by(
                EnergyMarketForecastModel.created_at.desc(),
            )
        )

        if market is not None:
            stmt = stmt.where(
                EnergyMarketForecastModel.market == market,
            )

        if variable is not None:
            stmt = stmt.where(
                EnergyMarketForecastModel.variable == variable,
            )

        return list(self.db_session.scalars(stmt))

    def get_forecast(
        self,
        forecast_id: int,
    ) -> EnergyMarketForecastModel | None:
        stmt = (
            select(EnergyMarketForecastModel)
            .options(*_EAGER_LOADS)
            .where(
                EnergyMarketForecastModel.id == forecast_id,
            )
        )

        return self.db_session.scalar(stmt)
