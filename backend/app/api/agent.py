from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

from app.api.dependencies import get_crm_service
from app.schemas.agent import LeadAnalysisResponse
from app.schemas.agent_request import LeadAnalysisRequest
from app.services.agent.revenue_ops import RevenueOpsAgent
from app.services.ai.gemini import GeminiService
from app.services.crm.service import CRMService
from app.tools.crm_tools import CRMTools
from app.schemas.action import ActionProposal
from app.services.agent.approval import ApprovalService
from app.services.agent.policy import ActionPolicy



router = APIRouter(
    prefix="/api/v1/agent",
    tags=["agent"]
)

@router.post(
    "/analyze/lead",
    response_model=LeadAnalysisResponse
)
async def analyze_lead(
    request: LeadAnalysisRequest,
    crm_service: CRMService = Depends(get_crm_service)
) -> LeadAnalysisResponse:
    """Analyze CRM leads using the RevenuOps agent."""
    
    crm_tools = CRMTools(
        crm_service
    )
    
    ai_service = GeminiService()
    
    agent = RevenueOpsAgent(
        crm_tools=crm_tools,
        ai_service=ai_service
    )
    
    try:
        analysis = await agent.analyze_lead(
            lead_id=request.lead_id
        )
    except ValueError as exec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exec)
        ) from exec
        
    return LeadAnalysisResponse(
        lead_id=request.lead_id,
        analysis=analysis,
    )
    
@router.post(
    "/propose-action/{lead_id}",
)
async def propose_action(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    crm_service: CRMService = Depends(
        get_crm_service
    ),
) -> dict[str, object]:
    """Analyze a lead and create an action proposal."""

    crm_tools = CRMTools(
        crm_service
    )

    ai_service = GeminiService()

    agent = RevenueOpsAgent(
        crm_tools=crm_tools,
        ai_service=ai_service,
    )

    proposal = await agent.propse_action(
        lead_id
    )

    policy = ActionPolicy()

    requires_approval = (
        policy.requires_approval(
            proposal.action
        )
    )

    if not requires_approval:
        return {
            "status": "ready",
            "proposal": proposal.model_dump(),
        }

    approval_service = ApprovalService(
        db
    )

    approval = (
        await approval_service.create_request(
            action=proposal.action,
            reason=proposal.reason,
        )
    )

    return {
        "status": "pending_approval",
        "approval_id": approval.id,
        "proposal": proposal.model_dump(),
    }