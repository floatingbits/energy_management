from fastapi import FastAPI

app = FastAPI(
    title="trading-service",
)


@app.get("/")
def root():
    return {"status": "ok", "service": "trading-service"}
