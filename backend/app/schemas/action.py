from typing import Literal

from pydantic import BaseModel, Field

ActionType = Literal[
    "create_follow_up_task",
    "update_lead_status"
]

class AgentAction(BaseModel):
    """Action proposed by the AI agent."""

    action_type: ActionType

    lead_id: int = Field(gt=0)

    priority: Literal[
        "low",
        "normal",
        "high",
    ] = "normal"

    title: str | None = None

    description: str | None = None

    new_status: Literal[
        "new",
        "contacted",
        "qualified",
        "unqualified",
        "converted",
    ] | None = None

    
    
class ActionProposal(BaseModel):
    """AI-generated action proposal."""

    action: AgentAction

    reason: str

    requires_approval: bool = True