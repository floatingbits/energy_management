# Energy Management

## Purpose
Exploration project to get an idea of the scope of a software engineer with machine learning tasks
in the field of direct marketing of renewable energies.

## Description
This project is supposed to simulate all the relevant aspects of an energy management platform:

- Forecasts (Energy pricing and production)
- Optimization (risk optimized trading recommendations)
- Event driven architecture
- Independent microservices (simulated in a mono repo)
- REST APIs
- Dashboard (Vue.js + echarts)
- Docker
- Necessary tools to operate the system in a safe and controlled way (Logging, Monitoring, Testing)

## Reached Milestones

- Micro Services communicating via RabbitMQ and REST
- OpenMeteo API implemented
- Structured persistence of forecasts
- First Dashboard with asset map and forecast chart
- First implementation of non-trivial power forecast strategies
- successful reality check/validation of first prediction: plausible results in good range for first shot.
Validation against [BR-PVGen dataset](https://zenodo.org/records/21511487). Prediction in peak times generally within 10%. 
Error metrics to follow.
- reflection on systematic improvement for PV prediction: Inverter types, tracker technologies, bifacial modules, 
diffuse radiation model, shadowing in off-peak-times
- static export of Dashboard UI deployed to [demo server](http://energy-dashboard.soerenparton.de/).
- first step towards uncertainty modeling: [prediction via LGBMRegressor](notebooks/03_uncertainty_modeling.ipynb)
- uncertainty modeling results in asset power forecasts and dashboard charts
- Asset power prediction error metrics for version 1 of physical model: 37% relative MAE (from 25% to 58% depending on 
actual asset). Further investigations derived from errors correlating with assets' metadata

![Showing a map, a panel for asset details and a chart that contains weather forecast information](./docs/images/energy_dashboard.png "Screenshot of Energy Management Dashboard")

## Next Steps

- Portfolio Aggregation reflecting error correlation of assets
- Wind Asset prediction
- Improving Prediction acccuracy of physical PV model (reflecting inverter types, bifaciality, improving diffuse model)
- energy price prediction

## Experiment Documentation
### PV Power forecast
![Shows a bar diagram of the evolving errors of pv power prediction](./docs/images/pv-power-forecast-error-evolution.svg "Evolution of error of pv power prediction")