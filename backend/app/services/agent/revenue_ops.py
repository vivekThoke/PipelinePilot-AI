from app.schemas.agent import LeadAnalysis
from app.services.ai.gemini import GeminiService
from app.tools.crm_tools import CRMTools


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