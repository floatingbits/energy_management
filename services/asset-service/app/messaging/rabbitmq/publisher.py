import pika

from event_contracts.base import BaseEvent
from app.messaging.publisher import EventPublisher

from app.messaging.rabbitmq.connection import create_connection


class RabbitMQPublisher(EventPublisher):

    QUEUE_NAME = "asset-events"


    def publish(
        self,
        event: BaseEvent
    ):

        connection = create_connection()

        try:
            channel = connection.channel()

            channel.queue_declare(
                queue=self.QUEUE_NAME,
                durable=True
            )

            channel.basic_publish(
                exchange="",
                routing_key=self.QUEUE_NAME,
                body=event.model_dump_json(),
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )

        finally:
            connection.close()