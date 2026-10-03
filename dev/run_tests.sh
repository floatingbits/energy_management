#!/bin/bash
for service in asset-service forecast-service; do
  docker compose exec --user=1000:1000 $service pytest  --junitxml=/artifacts/pytest.xml \
  --cov=app \
  --cov-report=xml:/artifacts/coverage.xml
done
