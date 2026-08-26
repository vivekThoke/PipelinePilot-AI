from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Lead
from app.schemas.lead import LeadResponse, LeadUpdate
from app.services.crm.service import CRMService


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
) -> list[LeadResponse]:
    """Return all CRM leads."""

    crm_service = CRMService(db)
    
    return await crm_service.list_leads()


@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
) -> LeadResponse:
    """Return a single CRM lead."""
    
    crm_service = CRMService(db)
    
    lead = await crm_service.get_lead(lead_id)
    
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

    crm_service = CRMService(db)
    
    lead = await crm_service.update_lead(
        lead_id=lead_id,
        lead_update=lead_update
    )
    
    if lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )
        
    return lead