import json
import pika

from event_contracts.asset_events import AssetCreatedEvent


def callback(
    channel,
    method,
    properties,
    body
):

    data = json.loads(body)

    event = AssetCreatedEvent(**data)

    print(
        "Received:",
        event
    )

    channel.basic_ack(
        delivery_tag=method.delivery_tag
    )


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
        queue="forecast.asset.created",
        durable=True
    )

    channel.queue_bind(
        exchange="energy.events",
        queue="forecast.asset.created",
        routing_key="asset.created"
    )


    channel.basic_consume(
        queue="forecast.asset.created",
        on_message_callback=callback
    )


    print("Waiting for messages...")

    channel.start_consuming()