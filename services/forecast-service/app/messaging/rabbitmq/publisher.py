import pika

from event_contracts.base import BaseEvent
from app.messaging.publisher import EventPublisher

from app.messaging.rabbitmq.connection import create_connection


class RabbitMQPublisher(EventPublisher):

    EXCHANGE_NAME = "energy.events"


    def publish(
        self,
        event: BaseEvent
    ):

        connection = create_connection()

        try:
            channel = connection.channel()

            channel.exchange_declare(
                exchange=self.EXCHANGE_NAME,
                exchange_type="topic",
                durable=True
            )

            channel.basic_publish(
                exchange=self.EXCHANGE_NAME,
                routing_key=event.event_type,
                body=event.model_dump_json(),
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )

        finally:
            connection.close()