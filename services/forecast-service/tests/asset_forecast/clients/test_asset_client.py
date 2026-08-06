import responses

from app.asset_forecast.clients.asset_client import AssetClient


@responses.activate
def test_get_asset():

    responses.add(
        responses.GET,
        "http://asset-service/assets/5",
        json={
            "id": 5,
            "name": "PV Hamburg",
            "asset_type": "solar",
            "latitude": 53.5,
            "longitude": 10.0,
            "pv_configuration": {
                "panel_area_m2": 50,
                "efficiency": 0.21,
                "tilt_deg": 30,
                "azimuth_deg": 180
            }
        },
        status=200,
    )


    client = AssetClient(
        base_url="http://asset-service"
    )


    result = client.get_asset(5)


    assert result["id"] == 5
    assert result["latitude"] == 53.5
    assert result["pv_configuration"]["tilt_deg"] == 30