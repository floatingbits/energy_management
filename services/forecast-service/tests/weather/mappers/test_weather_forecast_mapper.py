from datetime import datetime, timedelta

from app.forecasting.models import TimeSeriesValue, TimeSeries
from app.forecasting.models import TimeSeriesTimeBase
from app.forecasting.models.time_series_group import TimeSeriesGroup
from app.weather.mappers.weather_forecast_mapper import (
    WeatherForecastMapper,
)

from app.weather.models import WeatherForecast

from app.forecasting.enums import ForecastMetric
from app.forecasting.encoding.definitions import DEFAULT_QUANTILE_DEFINITION
from app.forecasting.encoding.serializers import serialize
from app.forecasting.domain.time_series_value import TimeSeriesValue as DomainTimeSeriesValue

def create_forecast_value(
        slot_index,
        value,
    ):
    return TimeSeriesValue(
        slot_index=slot_index,
        payload=serialize(
            DomainTimeSeriesValue(values=(None, value, None)),
            DEFAULT_QUANTILE_DEFINITION,
        ),
    )

def create_forecast_series(
        metric,
        values,
    ):
    return TimeSeries(
        metric=metric,
        values=values,
        value_type_definition=DEFAULT_QUANTILE_DEFINITION.serialize(),
    )
def test_maps_weather_forecast_model_to_domain():

    # Arrange

    db_values = [
        create_forecast_value(
            slot_index=0,
            value=500,
        ),
        create_forecast_value(
            slot_index=1,
            value=600,
        ),
    ]

    db_series = TimeSeries(
        metric=ForecastMetric.GLOBAL_SOLAR_IRRADIANCE,
        values=db_values,
        value_type_definition=DEFAULT_QUANTILE_DEFINITION.serialize(),
    )

    db_run = TimeSeriesTimeBase(
        start=datetime(2026, 8, 6, 12, 0),
        resolution_seconds=timedelta(minutes=15).total_seconds(),
        slots=2,
    )



    db_forecast = TimeSeriesGroup(
        time_series_time_base_id=1,
        time_series=[db_series]
    )

    db_forecast.time_series_time_base=db_run

    weather_model = WeatherForecast(
        forecast_id=1,
        latitude=53.5,
        longitude=10.0,
    )

    weather_model.forecast=db_forecast


    mapper = WeatherForecastMapper()


    # Act

    result = mapper.to_domain(
        weather_model
    )


    # Assert

    assert result.location.latitude == 53.5
    assert result.location.longitude == 10.0

    assert result.run.start == db_run.start
    assert result.run.slots == 2

    assert len(result.series) == 1

    series = result.series[0]

    assert (
        series.metric
        == ForecastMetric.GLOBAL_SOLAR_IRRADIANCE
    )

    assert len(series.values) == 2

    assert series.quantile(series.values[0], 50) == 500
    assert series.quantile(series.values[1], 50) == 600