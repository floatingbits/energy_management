from app.asset_forecast.calculators.plane_of_array_calculator import (
    PlaneOfArrayCalculator,
)
from app.asset_forecast.calculators.pv_power_calculator import (
    PvPowerCalculator,
)
from app.asset_forecast.calculators.solar_geometry_calculator import (
    SolarGeometryCalculator,
)
from app.asset_forecast.domain.panel_geometry import PanelGeometry
from app.asset_forecast.domain.pv_configuration import PvConfiguration
from app.asset_forecast.domain.pv_forecast import (
    PvForecastInput,
    PvForecastResult,
)


class PvForecastCalculator:

    def __init__(
        self,
        solar_geometry_calculator: SolarGeometryCalculator,
        plane_of_array_calculator: PlaneOfArrayCalculator,
        pv_power_calculator: PvPowerCalculator,
    ):
        self.solar_geometry_calculator = solar_geometry_calculator
        self.plane_of_array_calculator = plane_of_array_calculator
        self.pv_power_calculator = pv_power_calculator

    def calculate(
        self,
        forecast: PvForecastInput,
    ) -> PvForecastResult:

        solar_position = (
            self.solar_geometry_calculator.calculate(
                timestamp=forecast.timestamp,
                latitude=forecast.latitude,
                longitude=forecast.longitude,
            )
        )

        direct_irradiance = (
            self.plane_of_array_calculator.calculate(
                direct_normal_irradiance=forecast.direct_normal_irradiance,
                solar_position=solar_position,
                panel_geometry=forecast.panel_geometry,
            )
        )

        #
        # Erste Näherung:
        # diffuse Strahlung isotrop übernehmen.
        #

        total_irradiance = (
            direct_irradiance
            + forecast.diffuse_radiation
        )

        configuration = PvConfiguration(
            panel_area_m2=forecast.pv_configuration.panel_area_m2,
            efficiency=forecast.pv_configuration.efficiency,
        )

        active_power_kw = (
            self.pv_power_calculator.calculate(
                irradiance_w_m2=total_irradiance,
                configuration=configuration,
            )
        )

        return PvForecastResult(
            solar_position=solar_position,
            plane_of_array_irradiance=total_irradiance,
            active_power_kw=active_power_kw,
        )