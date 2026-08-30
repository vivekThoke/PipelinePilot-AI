from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from app.api.dependencies import get_crm_service
from app.schemas.agent import LeadAnalysisResponse
from app.schemas.agent_request import LeadAnalysisRequest
from app.services.agent.revenue_ops import RevenueOpsAgent
from app.services.ai.gemini import GeminiService
from app.services.crm.service import CRMService
from app.tools.crm_tools import CRMTools

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