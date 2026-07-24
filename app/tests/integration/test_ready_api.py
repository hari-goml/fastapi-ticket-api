from contextlib import asynccontextmanager

from fastapi.testclient import TestClient

from app.main import app


def test_ready_endpoint_returns_ready_status():
    @asynccontextmanager
    async def no_lifespan(app):
        yield

    app.router.lifespan_context = no_lifespan

    with TestClient(app) as client:
        response = client.get("/ready")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["service"] == "AI Ticket Service"
    assert "timestamp" in body