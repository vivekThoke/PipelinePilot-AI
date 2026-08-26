from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Lead
from app.schemas.lead import LeadResponse, LeadUpdate


router = APIRouter(
    prefix="/api/v1/leads",
    tags=["leads"],
)


@router.get(
    "",
    response_model=list[LeadResponse],
)
async def list_leads(
    db: AsyncSession = Depends(get_db),
) -> list[Lead]:
    """Return all CRM leads."""

    result = await db.execute(
        select(Lead).order_by(Lead.created_at.desc())
    )

    return list(result.scalars().all())


@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
) -> Lead:
    """Return a single CRM lead."""

    lead = await db.get(Lead, lead_id)

    if lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )

    return lead


@router.patch(
    "/{lead_id}",
    response_model=LeadResponse,
)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: AsyncSession = Depends(get_db),
) -> Lead:
    """Update allowed lead fields."""

    lead = await db.get(Lead, lead_id)

    if lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )

    update_data = lead_update.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(lead, field, value)

    await db.commit()
    await db.refresh(lead)

    return lead