from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str = (
        "postgresql+psycopg://trading:trading@trading-db:5432/tradingdb"
    )

    FORECAST_API_URL: str = "http://forecast-service:8000/api/v1"

    # Analogous to forecast-service's asset provider base URL.
    ASSET_API_URL: str = "http://asset-service:8000/api/v1"

    # Portfolio does not carry a market relation yet; decisions fall back
    # to this market until the asset-service models one ("DE-LU").
    DEFAULT_MARKET: str = "DE-LU"

    # Time zone of the delivery day grid (day-ahead market convention).
    DELIVERY_DAY_TZ: str = "Europe/Berlin"


settings = Settings()
