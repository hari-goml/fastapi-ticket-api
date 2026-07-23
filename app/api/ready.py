from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["Ready"])


@router.get("/ready")
async def ready():
    return {
        "status": "ready",
        "service": "AI Ticket Service",
        "timestamp": datetime.utcnow().isoformat(),
    }