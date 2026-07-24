import pytest
from pydantic import ValidationError

from app.schemas.ticket import SummarizeRequest, TicketCreate, TicketUpdate


def test_ticket_create_strips_whitespace_from_title():
    ticket = TicketCreate(title="  Login issue  ", priority="high")

    assert ticket.title == "Login issue"
    assert ticket.priority == "high"


def test_ticket_update_accepts_valid_status():
    ticket = TicketUpdate(status="resolved")
    assert ticket.status == "resolved"


def test_summarize_request_rejects_short_description():
    with pytest.raises(ValidationError):
        SummarizeRequest(ticket_description="short")

def test_ticket_create_rejects_special_characters():
    with pytest.raises(ValidationError):
        TicketCreate(
            title="@@@@!!!!",
            priority="high"
        )

def test_ticket_create_rejects_multiple_spaces():
    with pytest.raises(ValidationError):
        TicketCreate(
            title="Login    issue",
            priority="high"
        )
def test_ticket_create_rejects_emoji():
    with pytest.raises(ValidationError):
        TicketCreate(
            title="🔥 Login issue",
            priority="high"
        )