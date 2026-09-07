from app.schemas.agent import LeadAnalysis
from app.services.ai.gemini import GeminiService
from app.tools.crm_tools import CRMTools
from app.schemas.action import (
    ActionProposal,
    AgentAction
)


class RevenueOpsAgent:
    """AI agent responsible for Revenue Operations decisions."""

    def __init__(
        self,
        crm_tools: CRMTools,
        ai_service: GeminiService,
    ) -> None:
        self.crm_tools = crm_tools
        self.ai_service = ai_service

    async def analyze_lead(
        self,
        lead_id: int,
    ) -> LeadAnalysis:
        """Retrieve and analyze a CRM lead."""

        result = await self.crm_tools.get_lead(
            lead_id
        )

        if not result["success"]:
            raise ValueError("Lead not found")

        lead = result["lead"]

        if not isinstance(lead, dict):
            raise ValueError(
                "Invalid lead data returned from CRM"
            )

        return self.ai_service.analyze_lead(
            lead
        )
        
    async def propse_action(
        self,
        lead_id: int,
    ) -> ActionProposal:
        """Analyze a lead and propse a CRM action."""
        
        analysis = await self.analyze_lead(
            lead_id
        )
        
        if not analysis.should_create_task:
            return ActionProposal(
                action=AgentAction(
                    action_type=(
                        "update_lead_status"
                    ),
                    lead_id=lead_id,
                    new_status="new",
                ),
                reason=analysis.reasoning,
                requires_approval=True,
            )
            
        action = AgentAction(
            action_type="create_follow_up_task",
            lead_id=lead_id,
            priority=analysis.priority,
            title=analysis.task_title 
            or "Follow up with lead",
            description=analysis.task_description,
        )
        
        return ActionProposal(
            action=action,
            reason=analysis.reasoning,
            requires_approval=True
        )