from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Lead
from app.schemas.lead import LeadResponse, LeadUpdate
from app.services.crm.service import CRMService
from app.api.dependencies import get_crm_service


router = APIRouter(
    prefix="/api/v1/leads",
    tags=["leads"],
)


@router.get(
    "",
    response_model=list[LeadResponse],
)
async def list_leads(
    crm_service: CRMService = Depends(get_crm_service)
) -> list[LeadResponse]:
    """Return all CRM leads."""
    
    return await crm_service.list_leads()


@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
)
async def get_lead(
    lead_id: int,
    crm_service: CRMService = Depends(get_crm_service)
) -> LeadResponse:
    """Return a single CRM lead."""
    
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
    crm_service: CRMService = Depends(get_crm_service)
) -> Lead:
    """Update allowed lead fields."""

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