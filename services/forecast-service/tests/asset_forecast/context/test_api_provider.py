from unittest.mock import Mock

from app.asset_forecast.context.api_provider import ApiAssetContextProvider


def test_create_pv_asset_context():

    asset_client = Mock()

    asset_client.get_asset.return_value = {
        "id": 5,
        "latitude": 53.5,
        "longitude": 10.0,
        "configuration": {
            "panel_area_m2": 50,
            "efficiency": 0.21,
            "tilt_deg": 30,
            "azimuth_deg": 180,
        },
    }


    provider = ApiAssetContextProvider(
        asset_client
    )


    context = provider.get_pv_asset_context(
        5
    )


    assert context.asset_id == 5
    assert context.latitude == 53.5

    assert (
        context.panel_geometry.tilt_deg
        == 30
    )

    assert (
        context.pv_configuration.efficiency
        == 0.21
    )