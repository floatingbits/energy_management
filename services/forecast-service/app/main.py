import threading

from app.messaging.consumer import start_consumer
from app.api import app


def start_message_consumer():

    thread = threading.Thread(
        target=start_consumer,
        daemon=True
    )

    thread.start()


if __name__ == "__main__":

    start_message_consumer()

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )