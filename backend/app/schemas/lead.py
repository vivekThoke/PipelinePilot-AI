from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

class LeadResponse(BaseModel):
    """Lead returned by the CMR API."""
    
    id: int
    account_id: int
    name: str
    email: EmailStr | None
    job_title: str | None
    status: str
    source: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    
class LeadUpdate(BaseModel):
    """Feilds that can be updated for a lead"""
    
    status: str | None
    notes: str | None