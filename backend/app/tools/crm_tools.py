from app.schemas.lead import LeadStatus, LeadUpdate
from app.schemas.task import CreateTask, TaskPriority
from app.services.crm.service import CRMService


class CRMTools:
    """Controlled CRM operations available to the AI agent."""

    def __init__(
        self,
        crm_service: CRMService,
    ) -> None:
        self.crm_service = crm_service

    async def get_lead(
        self,
        lead_id: int,
    ) -> dict[str, object]:
        """Get information about a CRM lead."""

        lead = await self.crm_service.get_lead(
            lead_id
        )

        if lead is None:
            return {
                "success": False,
                "error": "Lead not found",
            }

        return {
            "success": True,
            "lead": {
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "job_title": lead.job_title,
                "status": lead.status,
                "source": lead.source,
                "notes": lead.notes,
            },
        }

    async def update_lead_status(
        self,
        lead_id: int,
        status: LeadStatus,
    ) -> dict[str, object]:
        """Update the status of a CRM lead."""

        lead = await self.crm_service.update_lead(
            lead_id,
            LeadUpdate(status=status),
        )

        if lead is None:
            return {
                "success": False,
                "error": "Lead not found",
            }

        return {
            "success": True,
            "lead_id": lead.id,
            "status": lead.status,
        }

    async def create_follow_up_task(
        self,
        lead_id: int,
        title: str,
        description: str | None = None,
        priority: TaskPriority = "normal",
    ) -> dict[str, object]:
        """Create a follow-up task for a lead."""

        task = await self.crm_service.create_task(
            CreateTask(
                lead_id=lead_id,
                title=title,
                description=description,
                priority=priority,
            )
        )

        if task is None:
            return {
                "success": False,
                "error": "Lead not found",
            }

        return {
            "success": True,
            "task": {
                "id": task.id,
                "lead_id": task.lead_id,
                "title": task.title,
                "priority": task.priority,
                "status": task.status,
            },
        }