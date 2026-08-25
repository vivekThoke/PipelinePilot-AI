from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.database import get_db

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/db")
async def database_health(
    db: AsyncSession = Depends(get_db), 
) -> dict[str, str]:
    """Check database connectivity."""
    
    await db.execute(text("SELECT 1"))
    
    return {"status": "ok"}