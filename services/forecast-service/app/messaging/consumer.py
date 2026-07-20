import json
import pika

from app.infrastructure.messaging import get_event_publisher
from event_contracts.asset_events import AssetCreatedEvent

from app.database import SessionLocal
from app.services import forecast_service

def callback(
    channel,
    method,
    properties,
    body
):

    event = AssetCreatedEvent.model_validate_json(
        body
    )

    db = SessionLocal()

    try:

        forecast_service.create_forecast_for_asset(
            db,
            event.asset_id,
            get_event_publisher()
        )

        print(
            f"Created forecast for asset {event.asset_id}"
        )


    finally:

        db.close()


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