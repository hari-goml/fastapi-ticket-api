from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
)
from app.services.ticket_service import (
    create_ticket,
    get_all,
    update_ticket,
    delete_ticket,
)
router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)

@router.post("/", response_model=TicketResponse)
async def create(
    ticket: TicketCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_ticket(db, ticket)



@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    status: str | None = None,
    priority: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await get_all(db, status, priority)


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update(
    ticket_id: UUID,
    data: TicketUpdate,
    db: AsyncSession = Depends(get_db),
):
    ticket = await update_ticket(db, ticket_id, data)
    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket



@router.delete("/{ticket_id}")
async def delete(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    deleted = await delete_ticket(db, ticket_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return {
        "message": "Ticket deleted successfully"
    }