from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.crm.service import CRMService

async def get_crm_service(
    db: AsyncSession = Depends(get_db),
) -> CRMService:
    """Provide a CRM service instance"""
    
    return CRMService(db)