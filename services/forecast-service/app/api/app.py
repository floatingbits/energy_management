from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

from app.api.forecasts import router as forecast_router


app = FastAPI(
    title="Asset Service",
    version="0.1.0"
)


app.include_router(
    forecast_router,
    prefix="/api/v1"
)


@app.get("/health")
def health():

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok"
    }