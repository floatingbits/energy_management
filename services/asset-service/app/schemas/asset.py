from datetime import datetime
from typing import Literal, Annotated

from pydantic import BaseModel, ConfigDict, Field
from app.enums import AssetType
from .configuration import (
    PvConfigurationResponse,
    WindConfigurationResponse,
    BatteryConfigurationResponse,
    PvConfigurationCreate,
    WindConfigurationCreate,
    BatteryConfigurationCreate,
)

class AssetBase(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=255
    )
    asset_type: AssetType
    installed_power_kw: float = Field(
        gt=0
    )
    latitude: float
    longitude: float
    status: str = "ACTIVE"


class AssetCreateBase(AssetBase):
    pass

class AssetResponseBase(AssetBase):

    id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class SolarAssetResponse(AssetResponseBase):

    asset_type: Literal[AssetType.SOLAR]

    configuration: PvConfigurationResponse


class WindAssetResponse(AssetResponseBase):

    asset_type: Literal[AssetType.WIND]

    configuration: WindConfigurationResponse


class BatteryAssetResponse(AssetResponseBase):

    asset_type: Literal[AssetType.BATTERY]

    configuration: BatteryConfigurationResponse


AssetResponse = Annotated[
    SolarAssetResponse
    | WindAssetResponse
    | BatteryAssetResponse,
    Field(discriminator="asset_type")
]


class AssetUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )

    asset_type: AssetType | None = None

    installed_power_kw: float | None = Field(
        default=None,
        gt=0
    )

    latitude: float | None = None

    longitude: float | None = None

    status: str | None = None


class SolarAssetCreate(AssetCreateBase):

    asset_type: Literal[AssetType.SOLAR]

    configuration: PvConfigurationCreate

class WindAssetCreate(AssetCreateBase):

    asset_type: Literal[AssetType.WIND]

    configuration: WindConfigurationCreate

class BatteryAssetCreate(AssetCreateBase):

    asset_type: Literal[AssetType.BATTERY]

    configuration: BatteryConfigurationCreate


AssetCreate = Annotated[
    SolarAssetCreate
    | WindAssetCreate
    | BatteryAssetCreate,
    Field(discriminator="asset_type")
]