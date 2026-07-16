from event_contracts.base import BaseEvent


class AssetCreatedEvent(BaseEvent):

    event_type: str = "AssetCreated"

    asset_id: int
    asset_type: str