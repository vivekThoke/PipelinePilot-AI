from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class ApprovalRequest(Base):
    """Pending agent action requiring human approval."""

    __tablename__ = "approval_requests"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    lead_id: Mapped[int] = mapped_column(
        nullable=False
    )

    action_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    action_payload: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )