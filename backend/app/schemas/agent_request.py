from pydantic import BaseModel, Field

class LeadAnalysisRequest(BaseModel):
    """Request to analyze a CRM lead."""
    
    lead_id: int = Field(
        gt=0
    )