from unittest.mock import AsyncMock

import pytest

from app.services.crm.service import CRMService
from app.tools.crm_tools import CRMTools


@pytest.mark.asyncio
async def test_get_lead_not_found() -> None:
    crm_service = AsyncMock(
        spec=CRMService
    )

    crm_service.get_lead.return_value = None

    crm_tools = CRMTools(crm_service)

    result = await crm_tools.get_lead(
        lead_id=999
    )

    assert result == {
        "success": False,
        "error": "Lead not found",
    }