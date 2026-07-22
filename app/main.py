from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.tickets import router
from app.core.database import engine
from app.models.base import Base
from app.models.ticket import Ticket
from app.middleware.logging import logging_middleware
from fastapi.middleware.cors import CORSMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)
app.middleware("http")(logging_middleware)
app.include_router(router)
origins = [
    "http://localhost:5173",
]

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