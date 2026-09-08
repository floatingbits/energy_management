class EventDispatcher:

    def __init__(self, handlers: dict):
        self.handlers = handlers

    def dispatch(self, event):
        handler = self.handlers.get(event.event_type)

        if handler is None:
            raise ValueError(
                f"No handler registered for event type "
                f"'{event.event_type}'"
            )

        handler.handle(event)