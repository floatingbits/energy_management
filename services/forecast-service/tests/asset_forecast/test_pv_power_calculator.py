from app.asset_forecast.calculators.pv_power_calculator import PvPowerCalculator
from app.asset_forecast.domain.pv_configuration import PvConfiguration


def test_pv_power_calculation():

    model = PvPowerCalculator()

    config = PvConfiguration(
        panel_area_m2=50,
        efficiency=0.2
    )


    result = model.calculate(
        irradiance_w_m2=1000,
        configuration=config
    )


    assert result == 10