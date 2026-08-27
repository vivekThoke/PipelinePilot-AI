import asyncio

from app.core.database import AsyncSessionLocal
from app.services.crm.service import CRMService
from app.tools.crm_tools import CRMTools


async def main() -> None:
    async with AsyncSessionLocal() as db:
        crm_service = CRMService(db)
        crm_tools = CRMTools(crm_service)

        result = await crm_tools.create_follow_up_task(
            lead_id=1,
            title="Follow up with John Smith",
            description="High-value enterprise prospect.",
            priority="high",
        )

        print(result)


if __name__ == "__main__":
     asyncio.run(
            main(),
            loop_factory=asyncio.SelectorEventLoop,
        )