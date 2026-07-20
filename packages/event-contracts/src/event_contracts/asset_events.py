from typing import Literal

from event_contracts.base import BaseEvent


class AssetCreatedEvent(BaseEvent):

    event_type: Literal["asset.created"] = "asset.created"

    asset_id: int
    asset_type: str