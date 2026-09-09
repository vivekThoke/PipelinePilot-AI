from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_crm_service
from app.core.database import get_db
from app.models import AuditLog
from app.schemas.approval import ApprovalResponse
from app.services.agent.approval import ApprovalService
from app.services.agent.executor import AgentActionExecutor
from app.services.crm.service import CRMService
from app.tools.crm_tools import CRMTools

router = APIRouter(
    prefix="/api/v1/approvals",
    tags=["approvals"]
)

@router.get(
    "/{approval_id}",
    response_model=ApprovalResponse,
)
async def get_approval(
    approval_id: int,
    db: AsyncSession = Depends(get_db),
) -> ApprovalResponse:
    """Get approval request"""
    
    service = ApprovalService(db)
    
    approval = await service.get_request(
        approval_id=approval_id
    )
    
    if approval is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found"
        )
        
    return approval

@router.post(
    "/{approval_id}/approve",
    response_model=ApprovalResponse
)
async def approve_section(
    approval_id: int,
    db: AsyncSession = Depends(get_db),
    crm_service: CRMService = Depends(
        get_crm_service
    ),
) -> ApprovalResponse:
    "Approve and execute an agent action."
    
    service = ApprovalService(db)
    
    approval = await service.get_request(
        approval_id
    )
    
    if approval is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found"
        )
        
    if approval.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Approval request already resolved"
            )
        )
        
    action = service.deserialize_action(
        approval
    )
    
    crm_tools = CRMTools(
        crm_service
    )
    
    executor = AgentActionExecutor(
        crm_tools
    )
    
    result = await executor.execute(
        action
    )
    
    if not result["success"]:
        approval.status = "failed"
        
        await db.commit()
        
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST,
            detail=str(result),
        )
        
    await service.mark_approved(
        approval
    )
    
    audit = AuditLog(
        action_type=action.action_type,
        lead_id=action.lead_id,
        status="success",
        details=str(result)
    )
    
    db.add(audit)
    
    await db.commit()
    
    return approval