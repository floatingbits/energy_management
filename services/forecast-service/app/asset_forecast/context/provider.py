from abc import ABC, abstractmethod

from app.asset_forecast.domain.pv_asset_context import (
    PvAssetContext,
)


class AssetContextProvider(ABC):

    @abstractmethod
    def get_pv_asset_context(
        self,
        asset_id: int,
    ) -> PvAssetContext:
        pass