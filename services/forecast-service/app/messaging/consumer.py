import pika

from event_contracts.base import BaseEvent

from app.bootstrap.events import (
    create_event_deserializer,
    create_event_dispatcher,
)


event_deserializer = create_event_deserializer()
event_dispatcher = create_event_dispatcher()

def callback(
    channel,
    method,
    properties,
    body
):

    try:
        event = event_deserializer.deserialize(body)
        event_dispatcher.dispatch(event)

        channel.basic_ack(
            delivery_tag=method.delivery_tag
        )

    except Exception:
        channel.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
        raise


def start_consumer():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq"
        )
    )

    channel = connection.channel()

    channel.exchange_declare(
        exchange="energy.events",
        exchange_type="topic",
        durable=True
    )

    channel.queue_declare(
        queue="forecast.asset",
        durable=True
    )

    channel.queue_bind(
        exchange="energy.events",
        queue="forecast.asset",
        routing_key="asset.*"
    )


    channel.basic_consume(
        queue="forecast.asset",
        on_message_callback=callback
    )


    print("Waiting for messages...")

    channel.start_consuming()