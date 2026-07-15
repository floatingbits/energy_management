import pika

from app.config import settings


def create_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(
        username=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD
    )

    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    )

    return pika.BlockingConnection(parameters)