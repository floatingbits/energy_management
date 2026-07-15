from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssetBase(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=255
    )
    asset_type: str
    installed_power_kw: float = Field(
        gt=0
    )
    latitude: float
    longitude: float
    status: str = "ACTIVE"


class AssetCreate(AssetBase):
    pass


class AssetResponse(AssetBase):

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )