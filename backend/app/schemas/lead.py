from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.action import AgentAction

LeadStatus = Literal[
    "new",
    "contacted",
    "qualified",
    "unqualified",
    "converted",
]

class LeadAnalysis(BaseModel):
    """Structured decision produced by the AI agent."""
    
    summary: str = Field(
        description="Short summary of the lead."
    )
    
    lead_quality: Literal[
        "low",
        "medium",
        "high"
    ]
    
    recommend_action: Literal[
        "follow_up",
        "qualify",
        "disqualify",
        "no_action"
    ]
    
    priority: Literal[
        "low",
        "normal",
        "high"
    ]
    
    resoning: str
    
    should_create_task: bool
    
    task_title: str | None = None
    
    task_description: str | None = None

class LeadResponse(BaseModel):
    """Lead returned by the CMR API."""
    
    id: int
    account_id: int
    name: str
    email: EmailStr | None
    job_title: str | None
    status: LeadStatus
    source: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    
class LeadUpdate(BaseModel):
    """Feilds that can be updated for a lead"""
    
    status: LeadStatus | None
    notes: str | None