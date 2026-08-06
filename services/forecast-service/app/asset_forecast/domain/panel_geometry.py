from dataclasses import dataclass


@dataclass(frozen=True)
class PanelGeometry:
    tilt_deg: float
    azimuth_deg: float