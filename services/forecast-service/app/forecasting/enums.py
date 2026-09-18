from enum import StrEnum


class ForecastMetric(StrEnum):
    WIND_SPEED = "wind_speed"
    TEMPERATURE = "temperature"
    CLOUD_COVER = "cloud_cover"
    GLOBAL_SOLAR_IRRADIANCE = "global_solar_irradiance"
    DIRECT_NORMAL_IRRADIANCE = "direct_normal_irradiance"
    DIFFUSE_IRRADIANCE = "diffuse_irradiance"
    WIND_DIRECTION = "wind_direction"
    PRECIPITATION = "precipitation"

    ACTIVE_POWER = "active_power"

    ELECTRICITY_PRICE = "electricity_price"

    DAY_AHEAD_ELECTRICITY_PRICE = "day_ahead_electricity_price"

    TOTAL_ENERGY_CONSUMPTION = "total_energy_consumption"


class ForecastValueType(StrEnum):
    FORECAST = "forecast"
    MEASURED = "measured"