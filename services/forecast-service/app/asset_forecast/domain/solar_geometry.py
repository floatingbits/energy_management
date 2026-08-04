from dataclasses import dataclass


@dataclass(frozen=True)
class SolarPosition:

    elevation_deg: float

    azimuth_deg: float