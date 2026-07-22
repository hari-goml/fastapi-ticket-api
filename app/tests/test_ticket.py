from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# def test_create_ticket_invalid_priority_type():
#     response = client.post(
#         "/tickets",
#         json={
#             "title": "Login Issue",
#             "priority": 123,
#             "status": "Open"
#         }
#     )

#     assert response.status_code == 422


def test_create_ticket_empty_title():
    response = client.post(
        "/tickets/",
        json={
            "title": "",
            "priority": "high",
            "status": "open"
        }
    )

    assert response.status_code == 422

    body = response.json()

    assert "Title cannot be empty" in str(body)

    