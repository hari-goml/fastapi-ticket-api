from app.services.aws.bedrock_service import FakeBedrockService


def test_fake_bedrock_service_formats_summary_and_response():
    service = FakeBedrockService()
    ticket_description = (
        "The application crashes when I try to export a very large report, and I need help quickly."
    )

    result = service.summarize_ticket(ticket_description)

    assert result["summary"] == f"Support issue: {ticket_description.strip()[:70]}"
    assert result["suggested_response"] == (
        "Acknowledge the issue, confirm that it is being investigated, and provide the next expected update."
    )