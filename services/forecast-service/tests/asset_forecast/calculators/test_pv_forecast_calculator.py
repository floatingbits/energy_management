from datetime import datetime, timezone
from dataclasses import replace
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
from app.asset_forecast.domain.pv_forecast import PvForecastInput


def test_pv_forecast_calculation():

    calculator = PvForecastCalculator(
        solar_geometry_calculator=SolarGeometryCalculator(),
        plane_of_array_calculator=PlaneOfArrayCalculator(),
        pv_power_calculator=PvPowerCalculator(),
    )
    forecast_input = PvForecastInput(
            timestamp=datetime(
                2026,
                6,
                21,
                12,
                0,
                tzinfo=timezone.utc,
            ),

            latitude=53.5,
            longitude=10.0,

            direct_normal_irradiance=900,
            diffuse_radiation=100,

            panel_geometry=PanelGeometry(
                tilt_deg=30,
                azimuth_deg=180,
            ),

            pv_configuration=PvConfiguration(
                panel_area_m2=50,
                efficiency=0.20,
            ),
        )
    result = calculator.calculate(
        forecast_input
    )

    # less efficient panel geometry: Facing north
    forecast_input2 = replace(forecast_input, panel_geometry=PanelGeometry(
                tilt_deg=30,
                azimuth_deg=0,
            )
    )

    result2 = calculator.calculate(
        forecast_input2
    )





    #
    # Sonnenstand plausibel
    #

    assert result.solar_position.elevation_deg > 50
    assert result.solar_position.azimuth_deg > 100

    #
    # Einstrahlung muss positiv sein
    #

    assert result.plane_of_array_irradiance > 500
    # Less efficient configuration in result2
    assert result.plane_of_array_irradiance > result2.plane_of_array_irradiance
    #
    # Leistung ebenfalls
    #

    assert result.active_power_kw > 0
    # Less efficient configuration in result2
    assert result.active_power_kw > result2.active_power_kw
    #
    # Physikalische Obergrenze:
    #
    # 1000 W/m² * 50 m² * 20 %
    # = 10 kW
    #

    assert result.active_power_kw < 10.5


def test_tilt_improves_power():

    calculator = PvForecastCalculator(
        solar_geometry_calculator=SolarGeometryCalculator(),
        plane_of_array_calculator=PlaneOfArrayCalculator(),
        pv_power_calculator=PvPowerCalculator(),
    )

    flat = calculator.calculate(
        PvForecastInput(
            timestamp=datetime(
                2026,
                6,
                21,
                12,
                tzinfo=timezone.utc,
            ),
            latitude=53.5,
            longitude=10.0,
            direct_normal_irradiance=900,
            diffuse_radiation=100,
            panel_geometry=PanelGeometry(
                tilt_deg=0,
                azimuth_deg=180,
            ),
            pv_configuration=PvConfiguration(
                panel_area_m2=50,
                efficiency=0.20,
            ),
        )
    )

    tilted = calculator.calculate(
        PvForecastInput(
            timestamp=datetime(
                2026,
                6,
                21,
                12,
                tzinfo=timezone.utc,
            ),
            latitude=53.5,
            longitude=10.0,
            direct_normal_irradiance=900,
            diffuse_radiation=100,
            panel_geometry=PanelGeometry(
                tilt_deg=30,
                azimuth_deg=180,
            ),
            pv_configuration=PvConfiguration(
                panel_area_m2=50,
                efficiency=0.20,
            ),
        )
    )

    assert tilted.active_power_kw > flat.active_power_kw