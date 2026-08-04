from dataclasses import dataclass

@dataclass(frozen=True)
class PvConfiguration:
    panel_area_m2: float
    efficiency: float