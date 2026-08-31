import asyncio

from app.core.database import AsyncSessionLocal
from app.services.agent.revenue_ops import RevenueOpsAgent
from app.services.ai.gemini import GeminiService
from app.services.crm.service import CRMService
from app.tools.crm_tools import CRMTools


async def main() -> None:
    async with AsyncSessionLocal() as db:
        crm_service = CRMService(db)

        crm_tools = CRMTools(
            crm_service
        )

        ai_service = GeminiService()

        agent = RevenueOpsAgent(
            crm_tools=crm_tools,
            ai_service=ai_service,
        )

        result = await agent.analyze_lead(
            lead_id=1,
        )

        print(
            result.model_dump_json(
                indent=2
            )
        )


if __name__ == "__main__":
     asyncio.run(
            main(),
            loop_factory=asyncio.SelectorEventLoop,
        )