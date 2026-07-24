from contextlib import asynccontextmanager

from fastapi.testclient import TestClient

from app.main import app


def test_root_endpoint_returns_service_message():
    @asynccontextmanager
    async def no_lifespan(app):
        yield

    app.router.lifespan_context = no_lifespan

    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Ticket API Running"}