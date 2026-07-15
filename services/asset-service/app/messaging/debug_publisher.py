from app.events.base import BaseEvent
from app.messaging.publisher import EventPublisher


class DebugEventPublisher:


    def publish(
        self,
        event: BaseEvent
    ):
        print(
            "EVENT:",
            event.model_dump()
        )

class FakeEventPublisher(EventPublisher):

    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)