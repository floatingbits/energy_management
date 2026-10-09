#!/bin/sh

set -eu

echo "Generating dependency graphs..."

pydeps \
    /projects/asset-service/app \
    --noshow \
    --dot-output /artifacts/asset-service.dot \
    -o /artifacts/asset-service.svg

pydeps \
    /projects/forecast-service/app \
    --noshow \
    --dot-output /artifacts/forecast-service.dot \
    -o /artifacts/forecast-service.svg

echo "Dependency graphs generated:"
ls -lh /artifacts/