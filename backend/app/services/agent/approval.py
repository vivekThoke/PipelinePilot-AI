import json
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ApprovalRequest
from app.schemas.action import AgentAction


class ApprovalService:
    """Manages human approval for agent actions."""

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def create_request(
        self,
        action: AgentAction,
        reason: str,
    ) -> ApprovalRequest:
        """Create a pending approval request."""

        approval = ApprovalRequest(
            lead_id=action.lead_id,
            action_type=action.action_type,
            action_payload=action.model_dump_json(),
            reason=reason,
            status="pending",
        )

        self.db.add(approval)

        await self.db.commit()
        await self.db.refresh(approval)

        return approval

    async def get_request(
        self,
        approval_id: int,
    ) -> ApprovalRequest | None:
        """Get an approval request."""

        return await self.db.get(
            ApprovalRequest,
            approval_id,
        )

    async def mark_approved(
        self,
        approval: ApprovalRequest,
    ) -> None:
        """Mark an approval request as approved."""

        approval.status = "approved"
        approval.resolved_at = datetime.utcnow()

        await self.db.commit()

    async def mark_rejected(
        self,
        approval: ApprovalRequest,
    ) -> None:
        """Mark an approval request as rejected."""

        approval.status = "rejected"
        approval.resolved_at = datetime.utcnow()

        await self.db.commit()

    @staticmethod
    def deserialize_action(
        approval: ApprovalRequest,
    ) -> AgentAction:
        """Deserialize the stored action."""

        payload = json.loads(
            approval.action_payload
        )

        return AgentAction.model_validate(
            payload
        )