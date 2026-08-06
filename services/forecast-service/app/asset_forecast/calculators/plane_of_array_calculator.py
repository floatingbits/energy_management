from math import cos
from math import radians
from math import sin

from app.asset_forecast.domain.panel_geometry import PanelGeometry
from app.asset_forecast.domain.solar_geometry import SolarPosition


class PlaneOfArrayCalculator:

    def calculate(
        self,
        direct_normal_irradiance: float,
        solar_position: SolarPosition,
        panel_geometry: PanelGeometry,
    ) -> float:

        cos_theta = self.cos_incidence_angle(
            solar_position,
            panel_geometry,
        )

        return max(
            0.0,
            direct_normal_irradiance * cos_theta
        )

    def cos_incidence_angle(
        self,
        solar_position: SolarPosition,
        panel_geometry: PanelGeometry,
    ) -> float:

        zenith = radians(
            90 - solar_position.elevation_deg
        )

        tilt = radians(
            panel_geometry.tilt_deg
        )

        solar_azimuth = radians(
            solar_position.azimuth_deg
        )

        panel_azimuth = radians(
            panel_geometry.azimuth_deg
        )

        return (
            cos(zenith)
            * cos(tilt)
            +
            sin(zenith)
            * sin(tilt)
            * cos(
                solar_azimuth
                -
                panel_azimuth
            )
        )