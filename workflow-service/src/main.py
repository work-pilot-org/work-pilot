from fastapi import FastAPI

from src.core.config import settings
from src.core.logging import logger
from src.infrastructure.database.session import engine
from src.infrastructure.database.session import engine
from src.modules.workflow.router import router as workflow_router


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow_router)
@app.on_event("startup")
async def startup():

    logger.info("Workflow Service Started")

    pass

@app.get("/")
async def root():

    return {
        "service": settings.APP_NAME,
        "status": "running",
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
    }