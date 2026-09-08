# packages/event-contracts/portfolio_events.py

from typing import Literal

from event_contracts.base import BaseEvent


class PortfolioCreatedEvent(BaseEvent):
    event_type: Literal["portfolio.created"] = "portfolio.created"

    portfolio_id: int


class PortfolioUpdatedEvent(BaseEvent):
    event_type: Literal["portfolio.updated"] = "portfolio.updated"

    portfolio_id: int
    changed_fields: list[str]


class PortfolioDeletedEvent(BaseEvent):
    event_type: Literal["portfolio.deleted"] = "portfolio.deleted"

    portfolio_id: int


class PortfolioMembershipChangedEvent(BaseEvent):
    event_type: Literal["portfolio.membership_changed"] = (
        "portfolio.membership_changed"
    )

    portfolio_id: int