from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CRMTask, Lead
from app.schemas.lead import LeadUpdate
from app.schemas.task import CreateTask


class CRMService:
    """Service responsible for CRM operations."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_leads(self) -> list[Lead]:
        """Return all leads."""

        result = await self.db.execute(
            select(Lead).order_by(
                Lead.created_at.desc()
            )
        )

        return list(result.scalars().all())

    async def get_lead(
        self,
        lead_id: int,
    ) -> Lead | None:
        """Return a lead by ID."""

        return await self.db.get(
            Lead,
            lead_id,
        )

    async def update_lead(
        self,
        lead_id: int,
        lead_update: LeadUpdate,
    ) -> Lead | None:
        """Update an existing lead."""

        lead = await self.get_lead(lead_id)

        if lead is None:
            return None

        update_data = lead_update.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(lead, field, value)

        await self.db.commit()
        await self.db.refresh(lead)

        return lead

    async def create_task(
        self,
        task_data: CreateTask,
    ) -> CRMTask | None:
        """Create a task for a lead."""

        lead = await self.get_lead(
            task_data.lead_id
        )

        if lead is None:
            return None

        task = CRMTask(
            **task_data.model_dump()
        )

        self.db.add(task)

        await self.db.commit()
        await self.db.refresh(task)

        return task