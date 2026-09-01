from unittest.mock import AsyncMock, Mock

import pytest

from app.schemas.agent import LeadAnalysis
from app.services.agent.revenue_ops import RevenueOpsAgent


@pytest.mark.asyncio
async def test_analyze_lead() -> None:
    crm_tools = AsyncMock()

    crm_tools.get_lead.return_value = {
        "success": True,
        "lead": {
            "id": 1,
            "name": "John Smith",
            "job_title": "VP of Operations",
            "status": "new",
        },
    }

    expected_analysis = LeadAnalysis(
        summary="High-value lead.",
        lead_quality="high",
        recommend_action="follow_up",
        priority="high",
        reasoning="VP-level contact with relevant interest.",
        should_create_task=True,
        task_title="Follow up with John Smith",
        task_description="Discuss next steps.",
    )

    ai_service = Mock()

    ai_service.analyze_lead.return_value = (
        expected_analysis
    )

    agent = RevenueOpsAgent(
        crm_tools=crm_tools,
        ai_service=ai_service,
    )

    result = await agent.analyze_lead(
        lead_id=1,
    )

    assert result == expected_analysis

    crm_tools.get_lead.assert_awaited_once_with(
        1
    )

    ai_service.analyze_lead.assert_called_once()
    
@pytest.mark.asyncio
async def test_analyze_missing_lead() -> None:
    crm_tools = AsyncMock()

    crm_tools.get_lead.return_value = {
        "success": False,
        "error": "Lead not found",
    }

    ai_service = Mock()

    agent = RevenueOpsAgent(
        crm_tools=crm_tools,
        ai_service=ai_service,
    )

    with pytest.raises(
        ValueError,
        match="Lead not found",
    ):
        await agent.analyze_lead(
            lead_id=999,
        )