from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
#from app.api.forecasts import router as forecast_router
from app.api.weather_forecasts import router as weather_router

from app.asset_forecast.router import (
    router as asset_forecast_router,
)


app = FastAPI(
    title="Forecast Service",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    asset_forecast_router,
    prefix="/api/v1"
)

# app.include_router(
#     forecast_router,
#     prefix="/api/v1"
# )

app.include_router(
    weather_router,
    prefix="/api/v1"
)


@app.get("/health")
def health():

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok"
    }