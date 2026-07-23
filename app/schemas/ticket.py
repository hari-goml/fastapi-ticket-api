from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
)


class TicketCreate(BaseModel):
    title: str
    priority: Literal["low", "medium", "high"]

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty")
        return value


class TicketUpdate(BaseModel):
    status: Literal["open", "in_progress", "resolved"] | None = None


class TicketResponse(BaseModel):
    id: UUID
    title: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "resolved"]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def is_resolved(self) -> bool:
        return self.status == "resolved"


class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=10, max_length=5000)


class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str