from fastapi import APIRouter, HTTPException, status
from fastapi import Request
from app.schemas.ticket import SummarizeRequest, SummarizeResponse
from app.services.aws.bedrock_service import (
    BedrockService,
    BedrockServiceError,
)

router = APIRouter(prefix="/ai", tags=["AI"])
@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_ticket(request: Request, payload: SummarizeRequest):
    service = request.app.state.bedrock_service
    return service.summarize_ticket(payload.ticket_description)