"""
WorkPilot AI Service
Application Entry Point.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from infrastructure.providers.http_client import http_client_provider

from .api.router import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown.
    """

    # Startup
    await http_client_provider.startup()

    yield

    # Shutdown
    await http_client_provider.shutdown()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(ai_router)


@app.get("/health")
async def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
    }


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to WorkPilot AI Service"
    }