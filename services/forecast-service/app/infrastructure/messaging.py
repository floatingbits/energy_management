from app.config import settings

from app.messaging.publisher import EventPublisher
from app.messaging.debug_publisher import DebugEventPublisher
from app.messaging.rabbitmq.publisher import RabbitMQPublisher


def get_event_publisher() -> EventPublisher:

    if settings.EVENT_BACKEND == "debug":
        return DebugEventPublisher()

    if settings.EVENT_BACKEND == "rabbitmq":
        return RabbitMQPublisher()

    raise RuntimeError("Unknown event backend")