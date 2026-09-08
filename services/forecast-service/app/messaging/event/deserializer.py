import json

from event_contracts.asset_events import (
    AssetCreatedEvent,
    AssetUpdatedEvent,
)
from event_contracts.base import BaseEvent


class EventDeserializer:

    def __init__(self, event_types: dict[str, type[BaseEvent]]):
        self.event_types = event_types

    def deserialize(self, body: bytes) -> BaseEvent:
        payload = json.loads(body)

        event_type = payload.get("event_type")

        if event_type is None:
            raise ValueError(
                "Event payload does not contain 'event_type'"
            )

        event_class = self.event_types.get(event_type)

        if event_class is None:
            raise ValueError(
                f"Unknown event type '{event_type}'"
            )

        return event_class.model_validate(payload)