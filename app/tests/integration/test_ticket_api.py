from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api import tickets as tickets_api
from app.core.database import get_db
from app.main import app



@asynccontextmanager
async def no_lifespan(app):
    yield


@contextmanager
def make_client(*, raise_server_exceptions: bool = True):
    app.router.lifespan_context = no_lifespan

    async def override_get_db():
        yield object()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app, raise_server_exceptions=raise_server_exceptions) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


def make_ticket(*, title: str, priority: str, status: str):
    return SimpleNamespace(
        id=uuid4(),
        title=title,
        priority=priority,
        status=status,
        created_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def client():
    with make_client() as test_client_instance:
        yield test_client_instance


def test_create_ticket_success(client, monkeypatch):
    async def fake_create_ticket(db, ticket):
        return make_ticket(title=ticket.title, priority=ticket.priority, status="open")

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
    assert body["is_resolved"] is False


def test_create_ticket_failure_returns_422(client):
    response = client.post(
        "/tickets/",
        json={"title": "Login issue", "priority": "urgent"},
    )

    assert response.status_code == 422


def test_list_tickets_success(client, monkeypatch):
    async def fake_get_all(db, status=None, priority=None):
        return [
            make_ticket(title="Login issue", priority="high", status="open"),
        ]

    monkeypatch.setattr(tickets_api, "get_all", fake_get_all)

    response = client.get("/tickets/?status=open")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Login issue"
    assert body[0]["status"] == "open"


def test_list_tickets_failure_returns_500(monkeypatch):
    async def fake_get_all(db, status=None, priority=None):
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(tickets_api, "get_all", fake_get_all)

    with make_client(raise_server_exceptions=False) as client_without_raise:
        response = client_without_raise.get("/tickets/")

    assert response.status_code == 500
    assert "Internal Server Error" in response.text


def test_update_ticket_success(client, monkeypatch):
    async def fake_update_ticket(db, ticket_id, data):
        return make_ticket(
            title="Login issue",
            priority="high",
            status=data.status or "open",
        )

    monkeypatch.setattr(tickets_api, "update_ticket", fake_update_ticket)

    response = client.put(
        f"/tickets/{uuid4()}",
        json={"status": "resolved"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "resolved"
    assert body["is_resolved"] is True


def test_update_ticket_failure_returns_404(client, monkeypatch):
    async def fake_update_ticket(db, ticket_id, data):
        return None
    monkeypatch.setattr(tickets_api, "update_ticket", fake_update_ticket)
    response = client.put(
        f"/tickets/{uuid4()}",
        json={"status": "resolved"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_delete_ticket_success(client, monkeypatch):
    async def fake_delete_ticket(db, ticket_id):
        return True

    monkeypatch.setattr(tickets_api, "delete_ticket", fake_delete_ticket)
    response = client.delete(f"/tickets/{uuid4()}")
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket deleted successfully"}


def test_delete_ticket_failure_returns_404(client, monkeypatch):
    async def fake_delete_ticket(db, ticket_id):
        return False

    monkeypatch.setattr(tickets_api, "delete_ticket", fake_delete_ticket)
    response = client.delete(f"/tickets/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"
