from app.asset_forecast.calculators.plane_of_array_calculator import (
    PlaneOfArrayCalculator
)

from app.asset_forecast.domain.panel_geometry import PanelGeometry
from app.asset_forecast.domain.solar_geometry import SolarPosition


def test_panel_facing_sun():

    calculator = PlaneOfArrayCalculator()

    position = SolarPosition(
        elevation_deg=60,
        azimuth_deg=180,
    )

    panel = PanelGeometry(
        tilt_deg=30,
        azimuth_deg=180,
    )

    result = calculator.calculate(
        direct_normal_irradiance=1000,
        solar_position=position,
        panel_geometry=panel,
    )

    assert result > 950