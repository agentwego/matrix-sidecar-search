from fastapi.testclient import TestClient

from matrix_sidecar_search.api import app


def test_healthz_returns_ok():
    client = TestClient(app)

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_endpoint_denies_without_user_id():
    client = TestClient(app)

    response = client.get("/search", params={"q": "Matrix"})

    assert response.status_code == 422


def test_search_endpoint_returns_empty_safe_default():
    client = TestClient(app)

    response = client.get("/search", params={"q": "Matrix", "user_id": "@alice:example.org"})

    assert response.status_code == 200
    assert response.json() == {"hits": [], "estimated_total_hits": 0}
