from datetime import datetime, timezone, timedelta

from app.asset_forecast.calculators.plane_of_array_calculator import (
    PlaneOfArrayCalculator,
)
from app.asset_forecast.calculators.pv_forecast_calculator import (
    PvForecastCalculator,
)
from app.asset_forecast.calculators.pv_power_calculator import (
    PvPowerCalculator,
)
from app.asset_forecast.calculators.solar_geometry_calculator import (
    SolarGeometryCalculator,
)

from app.asset_forecast.domain.panel_geometry import PanelGeometry
from app.asset_forecast.domain.pv_configuration import PvConfiguration
from app.asset_forecast.domain.pv_asset_context import PvAssetContext

from app.asset_forecast.generators.pv_asset_forecast_generator import (
    PvAssetForecastGenerator,
)

from app.forecasting.domain.forecast_run import ForecastRun
from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_value import ForecastValue
from app.forecasting.enums import ForecastMetric


from app.weather.result import WeatherLocationForecast
from app.weather.location import WeatherLocation

def test_generate_pv_asset_forecast():

    calculator = PvForecastCalculator(
        solar_geometry_calculator=SolarGeometryCalculator(),
        plane_of_array_calculator=PlaneOfArrayCalculator(),
        pv_power_calculator=PvPowerCalculator(),
    )

    generator = PvAssetForecastGenerator(
        forecast_calculator=calculator,
    )


    asset = PvAssetContext(
        asset_id=1,

        latitude=53.5,
        longitude=10.0,

        panel_geometry=PanelGeometry(
            tilt_deg=30,
            azimuth_deg=180,
        ),

        pv_configuration=PvConfiguration(
            panel_area_m2=50,
            efficiency=0.20,
        ),
    )


    run = ForecastRun(
        start=datetime(
            2026,
            6,
            21,
            12,
            tzinfo=timezone.utc,
        ),
        resolution=timedelta(seconds=900),
        slots=2,
    )


    dni_series = ForecastSeries(
        metric=ForecastMetric.DIRECT_NORMAL_IRRADIANCE,
        values=[
            ForecastValue(
                p50=900,
            ),
            ForecastValue(
                p50=850,
            ),
        ],
    )


    diffuse_series = ForecastSeries(
        metric=ForecastMetric.DIFFUSE_IRRADIANCE,
        values=[
            ForecastValue(
                p50=100,
            ),
            ForecastValue(
                p50=100,
            ),
        ],
    )

    dummy_location = WeatherLocation(0,0)
    weather_forecast = WeatherLocationForecast(
        location=dummy_location,
        run=run,
        series=[
            dni_series,
            diffuse_series,
        ],
    )


    result = generator.generate(
        asset,
        weather_forecast,
    )


    assert result.metric == ForecastMetric.ACTIVE_POWER

    assert len(result.values) == 2


    first_value = result.values[0]

    assert first_value.p50 is not None

    assert first_value.p50 > 0


    second_value = result.values[1]

    assert second_value.p50 > 0