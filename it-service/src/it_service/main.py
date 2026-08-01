from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from it_service.core.config import settings
from it_service.modules.access.router import router as access_router
from it_service.modules.assets.router import router as assets_router
from it_service.modules.devices.router import router as devices_router
from it_service.modules.helpdesk.router import router as helpdesk_router
from it_service.modules.licenses.router import router as licenses_router
from it_service.modules.maintenance.router import router as maintenance_router
from it_service.modules.software.router import router as software_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Routers
# ==========================================================

app.include_router(helpdesk_router)
app.include_router(assets_router)
app.include_router(devices_router)
app.include_router(software_router)
app.include_router(licenses_router)
app.include_router(access_router)
app.include_router(maintenance_router)


# ==========================================================
# Health Check
# ==========================================================

@app.get("/", tags=["Health"])
def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
    }