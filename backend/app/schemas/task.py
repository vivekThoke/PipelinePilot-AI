from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

TaskPriority = Literal[
    "low",
    "high",
    "normal"
]


class CreateTask(BaseModel):
    """Request to create CRM task."""   
    
    lead_id: int
    title: str
    description: str | None = None  
    priority: TaskPriority = "noraml"
    due_at: datetime | None = None
    
class TaskResponse(BaseModel):
    """CRM task returned by the API"""
    
    id: int
    lead_id: int
    title: str
    description: str | None
    priority: TaskPriority
    status: str
    due_at: datetime | None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)