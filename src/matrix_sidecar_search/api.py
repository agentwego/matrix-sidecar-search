from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from matrix_sidecar_search import __version__
from matrix_sidecar_search.config import Settings

app = FastAPI(title="Matrix Sidecar Search", version=__version__)


class SearchResponse(BaseModel):
    hits: list[dict] = Field(default_factory=list)
    estimated_total_hits: int = 0


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    settings = Settings()
    return {"status": "ok", "index_uid": settings.index_uid}


@app.get("/search")
def search(
    q: Annotated[str, Query(min_length=1)],
    user_id: Annotated[str, Query(min_length=1)],
) -> SearchResponse:
    """Safe default search endpoint.

    The deployed first slice exposes the endpoint but denies by omission until
    Synapse-backed visibility checks are wired into the request path.
    """

    _ = (q, user_id)
    return SearchResponse()
