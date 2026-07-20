from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class PortfolioCreate(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=255
    )

    description: str | None = None


class PortfolioResponse(BaseModel):

    id: int
    name: str
    description: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class PortfolioAssetResponse(BaseModel):

    portfolio_id: int
    asset_id: int
    model_config = ConfigDict(
        from_attributes=True
    )