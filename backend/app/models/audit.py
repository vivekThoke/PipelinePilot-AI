from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class AuditLog(Base):
    """Audit trail for agent actions."""
    
    __tablename__ = "audit_logs"
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    
    action_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    lead_id: Mapped[int | None] = mapped_column()
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    details: Mapped[str | None] = mapped_column(
        Text
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )