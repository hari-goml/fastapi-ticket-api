from contextlib import asynccontextmanager
from datetime import datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api import tickets as tickets_api
from app.core.database import get_db
from app.main import app


@pytest.fixture
def client():
    @asynccontextmanager
    async def no_lifespan(app):
        yield
    app.router.lifespan_context = no_lifespan

    async def override_get_db():
        yield object()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_ticket_endpoint_returns_ticket(client, monkeypatch):
    async def fake_create_ticket(db, ticket):
        return SimpleNamespace(
            id=uuid4(),
            title=ticket.title,
            priority=ticket.priority,
            status="open",
            created_at=datetime.now(),
        )

    monkeypatch.setattr(tickets_api, "create_ticket", fake_create_ticket)

    response = client.post(
        "/tickets/",
        json={"title": "Login issue", "priority": "high"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Login issue"
    assert body["priority"] == "high"
    assert body["status"] == "open"


def test_list_tickets_endpoint_returns_list(client, monkeypatch):
    async def fake_get_all(db, status=None, priority=None):
        return []

    monkeypatch.setattr(tickets_api, "get_all", fake_get_all)

    response = client.get("/tickets/")

    assert response.status_code == 200
    assert response.json() == []


def test_update_ticket_endpoint_returns_404_for_missing_ticket(client, monkeypatch):
    async def fake_update_ticket(db, ticket_id, data):
        return None

    monkeypatch.setattr(tickets_api, "update_ticket", fake_update_ticket)

    response = client.put(
        f"/tickets/{uuid4()}",
        json={"status": "resolved"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"
