# Project overview

This project models virtual power plants
and its energy forecasting workflows.

## Architecture

- It uses a microservice architecture in a mono repo
- Services live in docker containers, currently orchestrated by docker compose
- The services' code resides in repository_root/services
- Services communicate their state changes through Events. Currently implemented in RabbitMQ.
- Events communicate facts, not commands.
- Services can fetch detailed information about other service's data via REST API implemented in FastAPI
- PostgreSQL stores service-owned data. So the services in question have their own pgsql container
- A vue based dashboard resides in repository_root/frontend/dashboard-ui .
It shows a portfolio table/chooser and a map to choose assets. forecasts for the chosen asset and portfolio are fetched 
via REST from the respective services
- the asset-service is responsible for the asset and portfolio management. This is rather simple CRUD
- The forecast-service is responsible for creating and serving forecasts. 
Currently implemented: weather forecast (from API, run through a probability/quantile estimator), 
asset forecast (weather data quantiles run through simple physical model, only implemented for PV assets),
portfolio forecast (done via simple aggregation)


## Development

- Run services using Docker Compose.
- Run tests inside the relevant service container.
- Inspect existing patterns before introducing new ones.
- Leave system python untouched
- The repository_root's venv is made for dev tasks, such as repository_root/dev/export_static_api.py

## Constraints

- Do not introduce synchronous cross-service database access.
- Do not change public event schemas without discussing compatibility.