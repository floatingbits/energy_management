from app.weather.resolver import WeatherLocationResolver
from app.weather.location import WeatherLocation


def test_resolve_location():

    resolver = WeatherLocationResolver(
        grid_size=0.1
    )

    result = resolver.resolve(
        53.556789,
        10.012345
    )

    assert result == WeatherLocation(
        latitude=53.6,
        longitude=10.0
    )