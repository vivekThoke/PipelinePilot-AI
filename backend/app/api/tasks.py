from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import CRMTask, Lead
from app.schemas.task import CreateTask, TaskResponse


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["tasks"],
)


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def list_tasks(
    db: AsyncSession = Depends(get_db),
) -> list[CRMTask]:
    """Return all CRM tasks."""

    result = await db.execute(
        select(CRMTask).order_by(
            CRMTask.created_at.desc()
        )
    )

    return list(result.scalars().all())


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: CreateTask,
    db: AsyncSession = Depends(get_db),
) -> CRMTask:
    """Create a task for a lead."""

    lead = await db.get(
        Lead,
        task_data.lead_id,
    )

    if lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )

    task = CRMTask(
        **task_data.model_dump(),
    )

    db.add(task)

    await db.commit()
    await db.refresh(task)

    return task