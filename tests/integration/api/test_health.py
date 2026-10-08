import pytest
from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Service is healthy",
        "data": None,
    }


@pytest.mark.parametrize("path", ["/health/db", "/api/v1/health", "/api/v1/health/db"])
def test_removed_health_endpoints_return_404(client: TestClient, path: str) -> None:
    assert client.get(path).status_code == 404
