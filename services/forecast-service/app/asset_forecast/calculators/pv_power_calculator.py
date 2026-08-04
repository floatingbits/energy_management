from app.asset_forecast.domain.pv_configuration import PvConfiguration


class PvPowerCalculator:


    def calculate(
        self,
        irradiance_w_m2: float,
        configuration: PvConfiguration
    ) -> float:

        power_w = (
            irradiance_w_m2
            *
            configuration.panel_area_m2
            *
            configuration.efficiency
        )


        return power_w / 1000