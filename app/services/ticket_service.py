from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate

async def create_ticket(db: AsyncSession,data: TicketCreate) -> Ticket:
    ticket = Ticket(
        title=data.title,
        priority=data.priority,
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def get_all(
    db: AsyncSession,
    status: str | None = None,
    priority: str | None = None,
):
    stmt = select(Ticket)
    if status:
        stmt = stmt.where(Ticket.status == status)
    if priority:
        stmt = stmt.where(Ticket.priority == priority)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_ticket(db: AsyncSession,ticket_id: UUID):
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )

    return result.scalar_one_or_none()

async def update_ticket(db: AsyncSession,ticket_id: UUID,data: TicketUpdate):
    ticket = await get_ticket(db, ticket_id)
    if ticket is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ticket, key, value)

    await db.commit()
    await db.refresh(ticket)
    return ticket


async def delete_ticket(db: AsyncSession,ticket_id: UUID):
    ticket = await get_ticket(db, ticket_id)
    if ticket is None:
        return False
    await db.delete(ticket)
    await db.commit()
    return True