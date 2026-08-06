from dataclasses import dataclass

from app.asset_forecast.domain.panel_geometry import PanelGeometry
from app.asset_forecast.domain.pv_configuration import PvConfiguration


@dataclass(frozen=True)
class PvAssetContext:

    asset_id: int

    latitude: float
    longitude: float

    panel_geometry: PanelGeometry

    pv_configuration: PvConfiguration