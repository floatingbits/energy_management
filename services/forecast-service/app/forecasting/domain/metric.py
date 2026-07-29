from enum import StrEnum


class ForecastMetric(StrEnum):

    # Weather
    TEMPERATURE = "temperature"
    WIND_SPEED = "wind_speed"
    CLOUD_COVER = "cloud_cover"
    GLOBAL_RADIATION = "global_radiation"

    # Energy
    ACTIVE_POWER = "active_power"

    # Market
    ELECTRICITY_PRICE = "electricity_price"