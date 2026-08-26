from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import CRMTask, Lead
from app.schemas.task import CreateTask, TaskResponse
from app.services.crm.service import CRMService


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
) -> list[TaskResponse]:
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
) -> TaskResponse:
    """Create a task for a lead."""

    crm_serivce = CRMService(db)
    
    task = await crm_serivce.create_task(
        task_data
    )
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )
        
    return task