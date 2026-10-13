FROM python:3.12-slim

WORKDIR /app

ARG SERVICE_PATH

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ${SERVICE_PATH}/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY packages/event-contracts /tmp/event-contracts

RUN pip install /tmp/event-contracts

COPY packages/em-timeseries /tmp/em-timeseries

RUN pip install /tmp/em-timeseries

# For prod, where no volume is mounted and all is included in image
COPY ${SERVICE_PATH}/app ./app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
