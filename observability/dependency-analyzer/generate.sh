#!/bin/sh

set -eu

echo "Generating dependency graphs..."

pydeps \
    /projects/asset-service/app \
    --noshow \
    -o /artifacts/asset-service.svg

pydeps \
    /projects/forecast-service/app \
    --noshow \
    -o /artifacts/forecast-service.svg

echo "Dependency graphs generated:"
ls -lh /artifacts/