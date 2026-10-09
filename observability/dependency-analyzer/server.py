
from pathlib import Path

from fastapi import FastAPI, HTTPException

from parse_dot import parse_dot

app = FastAPI(title="Python Dependency Graph API")

ARTIFACT_DIR = Path("/artifacts")

SERVICES = {
    "asset-service": "asset-service.dot",
    "forecast-service": "forecast-service.dot",
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/dependencies/{service}")
def dependencies(service: str):
    filename = SERVICES.get(service)

    if filename is None:
        raise HTTPException(status_code=404, detail="Unknown service")

    path = ARTIFACT_DIR / filename

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Graph not generated: {filename}",
        )

    try:
        return parse_dot(path)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not parse DOT graph: {exc}",
        ) from exc