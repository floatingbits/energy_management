from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    EVENT_BACKEND: str = "debug"
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str


settings = Settings()