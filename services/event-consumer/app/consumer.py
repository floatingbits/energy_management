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

    channel.queue_declare(
        queue="asset-events",
        durable=True
    )


    channel.basic_consume(
        queue="asset-events",
        on_message_callback=callback
    )


    print("Waiting for messages...")

    channel.start_consuming()