from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    event_type: str
    schema_version: int = 1