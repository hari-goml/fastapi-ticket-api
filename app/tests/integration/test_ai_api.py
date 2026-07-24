from contextlib import asynccontextmanager

from fastapi.testclient import TestClient

from app.main import app


class DummyBedrockService:
    def summarize_ticket(self, ticket_description):
        return {
            "summary": "Short summary",
            "suggested_response": "Suggested reply",
        }


def test_ai_summarize_endpoint_returns_summary():
    @asynccontextmanager
    async def no_lifespan(app):
        yield

    app.router.lifespan_context = no_lifespan
    app.state.bedrock_service = DummyBedrockService()

    with TestClient(app) as client:
        response = client.post(
            "/ai/summarize",
            json={"ticket_description": "The app crashes when I click save."},
        )

    assert response.status_code == 200
    assert response.json() == {
        "summary": "Short summary",
        "suggested_response": "Suggested reply",
    }