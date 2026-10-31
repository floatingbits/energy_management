#!/bin/bash
# Todo, should be done via requirements, but listening to asset created event seemed to have failed.
docker compose exec forecast-service python -m app.jobs.run_weather_forecast
docker compose exec forecast-service python -m app.jobs.generate_asset_forecast
docker compose exec forecast-service python -m app.cli.portfolio_forecast_updater
docker compose exec forecast-service python -m app.jobs.generate_energy_market_forecast