from app.events.base import BaseEvent


class EventPublisher:


    def publish(
        self,
        event: BaseEvent
    ):
        raise NotImplementedError