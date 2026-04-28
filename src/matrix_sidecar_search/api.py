from fastapi import FastAPI

from matrix_sidecar_search import __version__
from matrix_sidecar_search.config import Settings

app = FastAPI(title="Matrix Sidecar Search", version=__version__)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    settings = Settings()
    return {"status": "ok", "index_uid": settings.index_uid}
