from fastapi import FastAPI


app = FastAPI(
    title="PipelinePilot AI",
    description="An agentic revenue operations assistant",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}