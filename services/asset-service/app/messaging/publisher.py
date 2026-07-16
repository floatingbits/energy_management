from event_contracts.base import BaseEvent


class EventPublisher:


    def publish(
        self,
        event: BaseEvent
    ):
        raise NotImplementedError