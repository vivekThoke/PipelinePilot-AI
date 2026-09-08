from datetime import datetime

from pydantic import BaseModel

class ApprovalResponse(BaseModel):
    """Approval request returned by the API."""
    
    id: int
    lead_id: int
    action_type: str
    reason: str
    status: str
    created_at: datetime
    resolved_at: datetime | None
    
    class Config:
        from_attributes = True