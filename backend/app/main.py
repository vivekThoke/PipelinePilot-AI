from fastapi import FastAPI
from app.api.health import router as db_health_router
from app.api.leads import router as leads_router
from app.api.tasks import router as tasks_router

app = FastAPI(
    title="PipelinePilot AI",
    description="An agentic revenue operations assistant",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(db_health_router)
app.include_router(leads_router)
app.include_router(tasks_router)