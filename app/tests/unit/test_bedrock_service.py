import json
from unittest.mock import Mock

import pytest

from app.services.aws.bedrock_service import BedrockService, BedrockServiceError


def test_summarize_ticket_success():
    mock_client = Mock()

    mock_client.converse.return_value = {
        "output": {
            "message": {
                "content": [
                    {
                        "text": json.dumps({
                            "summary": "Internet issue",
                            "suggested_response": "Restart the router",
                        })
                    }
                ]
            }
        }
    }

    service = BedrockService(client=mock_client)
    result = service.summarize_ticket("My internet is not working.")
    assert result["summary"] == "Internet issue"
    assert result["suggested_response"] == "Restart the router"

def test_summarize_ticket_invalid_response_raises_error():
    mock_client = Mock()
    mock_client.converse.return_value = {
        "output": {
            "message": {
                "content": [{"text": "not valid json"}]
            }
        }
    }

    service = BedrockService(client=mock_client)

    with pytest.raises(BedrockServiceError, match="invalid response"):
        service.summarize_ticket("My internet is not working.")