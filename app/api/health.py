from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
            },
        )