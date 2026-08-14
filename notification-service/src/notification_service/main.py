from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from notification_service.modules.notifications.internal_router import (
    internal_router,
)

from notification_service.modules.notifications.router import (
    router as notifications_router,
)
from shared_infrastructure.core.config import settings


app = FastAPI(
    title="WorkPilot Notification Service",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(notifications_router)
app.include_router(internal_router)
@app.get("/", tags=["Health"])
def root():
    return {
        "service": "WorkPilot Notification Service",
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "WorkPilot Notification Service",
    }