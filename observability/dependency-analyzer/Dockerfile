FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pydeps

WORKDIR /workspace

COPY generate.sh /usr/local/bin/generate-dependencies

RUN chmod +x /usr/local/bin/generate-dependencies

ENTRYPOINT ["generate-dependencies"]