from datetime import datetime, timedelta

from app.forecasting.models import ForecastValue, ForecastSeries
from app.forecasting.models import ForecastRun
from app.forecasting.models.forecast import Forecast
from app.weather.mappers.weather_forecast_mapper import (
    WeatherForecastMapper,
)

from app.weather.models import WeatherForecast

from app.forecasting.enums import ForecastMetric

def create_forecast_value(
        slot_index,
        value,
    ):
    return ForecastValue(
        slot_index=slot_index,
        p50=value,
        p05=None,
        p95=None,
    )

def create_forecast_series(
        metric,
        values,
    ):
    return ForecastSeries(
        metric=metric,
        values=[]
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

    db_series = ForecastSeries(
        metric=ForecastMetric.GLOBAL_SOLAR_IRRADIANCE,
        values=db_values,
    )

    db_run = ForecastRun(
        start=datetime(2026, 8, 6, 12, 0),
        resolution_seconds=timedelta(minutes=15).total_seconds(),
        slots=2,
    )



    db_forecast = Forecast(
        forecast_run_id=1,
        series=[db_series]
    )

    db_forecast.forecast_run=db_run

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

    assert series.values[0].p50 == 500
    assert series.values[1].p50 == 600