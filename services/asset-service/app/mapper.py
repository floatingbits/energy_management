from app.enums import AssetType

from app.models import Asset

from app.schemas.asset import (
    AssetResponse,
    SolarAssetResponse,
    WindAssetResponse,
    BatteryAssetResponse,
)

from app.models.configuration import (
    PvConfiguration,
    WindConfiguration,
    BatteryConfiguration,
)

from app.schemas.asset import AssetCreate


def to_response(asset: Asset) -> AssetResponse:

    if asset.asset_type == AssetType.SOLAR:

        return SolarAssetResponse.model_validate(
            {
                **asset.__dict__,
                "configuration": asset.pv_configuration,
            }
        )


    if asset.asset_type == AssetType.WIND:

        return WindAssetResponse.model_validate(
            {
                **asset.__dict__,
                "configuration": asset.wind_configuration,
            }
        )


    if asset.asset_type == AssetType.BATTERY:

        return BatteryAssetResponse.model_validate(
            {
                **asset.__dict__,
                "configuration": asset.battery_configuration,
            }
        )


    raise ValueError(
        f"Unsupported asset type: {asset.asset_type}"
    )

def to_response_list(
    assets: list[Asset]
) -> list[AssetResponse]:

    return [
        to_response(asset)
        for asset in assets
    ]


def create_asset_model(
    data: AssetCreate
) -> Asset:

    asset = Asset(
        name=data.name,
        latitude=data.latitude,
        longitude=data.longitude,
        installed_power_kw=data.installed_power_kw,
        asset_type=data.asset_type,
    )


    if data.asset_type == AssetType.SOLAR:

        asset.pv_configuration = PvConfiguration(
            **data.configuration.model_dump()
        )


    elif data.asset_type == AssetType.WIND:

        asset.wind_configuration = WindConfiguration(
            **data.configuration.model_dump()
        )


    elif data.asset_type == AssetType.BATTERY:

        asset.battery_configuration = BatteryConfiguration(
            **data.configuration.model_dump()
        )


    else:
        raise ValueError(
            f"Unsupported asset type {data.asset_type}"
        )


    return asset