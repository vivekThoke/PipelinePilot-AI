from typing import Literal

from pydantic import BaseModel, Field

class LeadAnalysis(BaseModel):
    """Structured decision produced by the AI agents."""
    
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
        "no_action",
    ]
    
    priority: Literal[
        "low",
        "normal",
        "high",
    ]
    
    reasoning: str = Field(
        description=(
            "Explantion based only on the avliable lead information"
        )
    )
    
    should_create_task: bool
    
    task_title: str | None = None
    
    task_description: str | None = None