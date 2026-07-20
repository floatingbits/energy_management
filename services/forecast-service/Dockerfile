FROM python:3.12-slim

WORKDIR /app

ARG SERVICE_PATH


COPY ${SERVICE_PATH}/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY packages/event-contracts /tmp/event-contracts

RUN pip install /tmp/event-contracts

# For prod, where no volume is mounted and all is included in image
COPY ${SERVICE_PATH}/app ./app


CMD ["python","-u","-m","app.main"]