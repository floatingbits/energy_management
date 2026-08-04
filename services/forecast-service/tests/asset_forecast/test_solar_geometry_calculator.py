from app.asset_forecast.calculators.solar_geometry_calculator import SolarGeometryCalculator
from datetime import datetime, timezone

def test_solar_position_in_hamburg_summer():

    calculator = SolarGeometryCalculator()

    result = calculator.calculate(
        timestamp=datetime(
            2026,
            6,
            21,
            12,
            tzinfo=timezone.utc
        ),
        latitude=53.5,
        longitude=10.0
    )

    assert result.elevation_deg > 40
    assert result.elevation_deg < 70