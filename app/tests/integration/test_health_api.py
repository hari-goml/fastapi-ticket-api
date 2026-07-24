from contextlib import asynccontextmanager

from fastapi.testclient import TestClient

from app.api import health as health_api
from app.main import app


class DummySession:
    async def execute(self, query):
        return None


class DummySessionLocal:
    async def __aenter__(self):
        return DummySession()
    async def __aexit__(self, exc_type, exc, tb):
        return False


def test_health_endpoint_returns_connected_status(monkeypatch):
    @asynccontextmanager
    async def no_lifespan(app):
        yield

    app.router.lifespan_context = no_lifespan
    monkeypatch.setattr(health_api, "AsyncSessionLocal", lambda: DummySessionLocal())

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["database"] == "connected"
    assert "timestamp" in body