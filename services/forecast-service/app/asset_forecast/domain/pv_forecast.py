from dataclasses import dataclass
from datetime import datetime

from app.asset_forecast.domain.panel_geometry import PanelGeometry
from app.asset_forecast.domain.pv_configuration import PvConfiguration
from app.asset_forecast.domain.solar_geometry import SolarPosition

@dataclass(frozen=True)
class PvForecastInput:
    timestamp: datetime

    latitude: float
    longitude: float

    direct_normal_irradiance: float
    diffuse_radiation: float

    panel_geometry: PanelGeometry

    pv_configuration: PvConfiguration



@dataclass(frozen=True)
class PvForecastResult:
    solar_position: SolarPosition
    plane_of_array_irradiance: float
    active_power_kw: float