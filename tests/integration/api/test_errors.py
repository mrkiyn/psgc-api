from fastapi.testclient import TestClient


def test_unknown_route_returns_enveloped_404(client: TestClient) -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {"success": False, "message": "Not Found", "data": None}


def test_wrong_method_returns_enveloped_405(client: TestClient) -> None:
    response = client.post("/health")

    assert response.status_code == 405
    assert response.json() == {"success": False, "message": "Method Not Allowed", "data": None}
