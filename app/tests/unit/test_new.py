import pytest
from pydantic import ValidationError
from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    SummarizeRequest,
)

@pytest.fixture
def valid_ticket():
    return {
        "title": "Unable to login",
        "description": "User cannot login to the application.",
        "priority": "high",
        "status": "open",
    }

def test_create_ticket_valid(valid_ticket):
    ticket = TicketCreate(**valid_ticket)
    assert ticket.title == "Unable to login"
    assert ticket.priority == "high"


@pytest.mark.parametrize("title", [
    "",
    " ",
    "   ",
])
def test_create_ticket_invalid_title(title, valid_ticket):
    valid_ticket["title"] = title
    with pytest.raises(ValidationError):
        TicketCreate(**valid_ticket)

@pytest.mark.parametrize("priority", [
    "urgent",
    "critical",
    "very-high",
])
def test_create_ticket_invalid_priority(priority, valid_ticket):
    valid_ticket["priority"] = priority
    with pytest.raises(ValidationError):
        TicketCreate(**valid_ticket)

def test_update_ticket_valid():
    ticket = TicketUpdate(status="in_progress")
    assert ticket.status == "in_progress"

@pytest.mark.parametrize("status", [
    "DONE",
    "FINISHED",
    "INVALID",
])
def test_update_ticket_invalid_status(status):
    with pytest.raises(ValidationError):
        TicketUpdate(status=status)

def test_summarize_request_valid():
    request = SummarizeRequest(
        ticket_description="My laptop is overheating."
    )
    assert request.ticket_description == "My laptop is overheating."

def test_summarize_request_too_short():
    with pytest.raises(ValidationError):
        SummarizeRequest(ticket_description="short")