from typing import Literal

from event_contracts.base import BaseEvent


class AssetCreatedEvent(BaseEvent):

    event_type: Literal["asset.created"] = "asset.created"

    asset_id: int
    asset_type: str

class AssetUpdatedEvent(BaseEvent):
    event_type: Literal["asset.updated"] = "asset.updated"

    asset_id: int
    changed_fields: list[str]


class AssetDeletedEvent(BaseEvent):
    event_type: Literal["asset.deleted"] = "asset.deleted"

    asset_id: int