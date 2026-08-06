from unittest.mock import Mock

from app.asset_forecast.service import (
    AssetForecastService,
)


def test_generate_asset_forecast():

    asset_provider = Mock()

    weather_service = Mock()

    generator = Mock()


    asset_context = Mock()
    asset_context.latitude = 53.5
    asset_context.longitude = 10.0


    asset_provider.get_pv_asset_context.return_value = (
        asset_context
    )


    db_weather_forecast = Mock()

    weather_service.get_weather_forecasts.return_value = (
        [db_weather_forecast]
    )


    expected_series = Mock()

    generator.generate.return_value = (
        expected_series
    )

    weather_forecast = Mock()
    domain_mapper = Mock()
    domain_mapper.to_domain.return_value = (
        weather_forecast
    )


    expected_db_asset_forecast = Mock()

    asset_forecast_repository = Mock()
    asset_forecast_repository.save.return_value = expected_db_asset_forecast
    service = AssetForecastService(
        asset_context_provider=asset_provider,
        domain_mapper=domain_mapper,
        weather_service=weather_service,
        pv_forecast_generator=generator,
        asset_forecast_repository=asset_forecast_repository
    )


    result = service.generate(
        asset_id=5
    )


    assert result == expected_db_asset_forecast


    asset_provider.get_pv_asset_context.assert_called_once_with(
        5
    )


    weather_service.get_weather_forecasts.assert_called_once_with(
        53.5,
        10.0,
        1
    )


    generator.generate.assert_called_once_with(
        asset_context,
        weather_forecast,
    )