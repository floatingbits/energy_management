from app.asset_forecast.context.provider import AssetContextProvider
from app.asset_forecast.domain.pv_asset_context import (
    PvAssetContext,
)

from app.asset_forecast.domain.panel_geometry import (
    PanelGeometry,
)

from app.asset_forecast.domain.pv_configuration import (
    PvConfiguration,
)


class ApiAssetContextProvider(AssetContextProvider):

    def __init__(
        self,
        asset_client,
    ):
        self.asset_client = asset_client


    def get_pv_asset_context(
        self,
        asset_id: int,
    ) -> PvAssetContext:

        asset = self.asset_client.get_asset(
            asset_id
        )

        return PvAssetContext(

            asset_id=asset["id"],

            latitude=asset["latitude"],
            longitude=asset["longitude"],

            panel_geometry=PanelGeometry(
                tilt_deg=asset["configuration"]["tilt_deg"],
                azimuth_deg=asset["configuration"]["azimuth_deg"],
            ),

            pv_configuration=PvConfiguration(
                panel_area_m2=asset["configuration"]["panel_area_m2"],
                efficiency=asset["configuration"]["efficiency"],
            ),
        )