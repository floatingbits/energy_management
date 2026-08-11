FROM python:3.12-slim

WORKDIR /app

ARG SERVICE_PATH

# lightgbm needs this shared library
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*


COPY ${SERVICE_PATH}/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY packages/event-contracts /tmp/event-contracts

RUN pip install /tmp/event-contracts

# For prod, where no volume is mounted and all is included in image
COPY ${SERVICE_PATH}/app ./app


CMD ["python","-u","-m","app.main"]