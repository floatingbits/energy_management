from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )

    event_type: str