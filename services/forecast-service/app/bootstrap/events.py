from app.bootstrap.forecast_requirements import (
    create_asset_forecast_requirement_service,
)

from app.messaging.event.deserializer import EventDeserializer
from app.messaging.event_dispatcher import  EventDispatcher

from app.messaging.handlers.asset import (
     AssetForecastRequirementHandler
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
            "asset.created": AssetForecastRequirementHandler(
                requirement_service=
                    create_asset_forecast_requirement_service()
            ),
            "asset.updated": AssetForecastRequirementHandler(
                requirement_service=
                    create_asset_forecast_requirement_service()
            ),
        }
    )