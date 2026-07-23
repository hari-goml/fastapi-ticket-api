from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.tickets import router
from app.core.database import engine
from app.models.base import Base
from app.models.ticket import Ticket
from app.middleware.logging import logging_middleware
from fastapi.middleware.cors import CORSMiddleware
from app.api.ai import router as ai_router
from app.api.health import router as health_router
from app.api.ready import router as ready_router
from app.services.aws.bedrock_service import BedrockService
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    app.state.bedrock_service = BedrockService()
    

    yield

app = FastAPI(lifespan=lifespan)
app.middleware("http")(logging_middleware)
app.include_router(router)
app.include_router(health_router)
app.include_router(ready_router)
origins = [
    "http://localhost:5173",
]
app.include_router(ai_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {
        "message": "Ticket API Running"
    }