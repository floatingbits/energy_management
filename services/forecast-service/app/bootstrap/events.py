from app.bootstrap.asset_forecast import (
    create_asset_forecast_service,
)
from app.bootstrap.forecast_requirements import (
    create_asset_forecast_requirement_service,
)

from app.messaging.event.deserializer import EventDeserializer
from app.messaging.event_dispatcher import  EventDispatcher

from app.messaging.handlers.asset import (
    AssetCreatedHandler,
)
from app.messaging.handlers.asset import (
    AssetUpdatedHandler,
)

from event_contracts.asset_events import (
    AssetCreatedEvent,
    AssetUpdatedEvent,
)


def create_event_deserializer():

    return EventDeserializer(
        {
            "asset.created": AssetCreatedEvent,
            "asset.updated": AssetUpdatedEvent,
        }
    )


def create_event_dispatcher():

    return EventDispatcher(
        {
            "asset.created": AssetCreatedHandler(
                asset_forecast_service=
                    create_asset_forecast_service()
            ),
            "asset.updated": AssetUpdatedHandler(
                requirement_service=
                    create_asset_forecast_requirement_service()
            ),
        }
    )