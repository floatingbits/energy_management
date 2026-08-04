from datetime import datetime

from pysolar.solar import get_altitude
from pysolar.solar import get_azimuth

from app.asset_forecast.domain.solar_geometry import SolarPosition


class SolarGeometryCalculator:


    def calculate(
        self,
        timestamp: datetime,
        latitude: float,
        longitude: float,
    ) -> SolarPosition:

        return SolarPosition(
            elevation_deg=get_altitude(
                latitude,
                longitude,
                timestamp
            ),

            azimuth_deg=get_azimuth(
                latitude,
                longitude,
                timestamp
            )
        )