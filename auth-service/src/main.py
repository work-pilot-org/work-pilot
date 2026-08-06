from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from shared_infrastructure.core.config import settings
from src.modules.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from shared_infrastructure.core.exceptions import WorkPilotException
from src.infrastructure.middleware.tenant_middleware import TenantMiddleware
from src.modules.invitation.router import router as invitation_router
from src.modules.invitation.internal_router import internal_router as invitation_internal_router

app = FastAPI(
    title=settings.APP_NAME,
)

@app.exception_handler(WorkPilotException)
async def workpilot_exception_handler(request: Request, exc: WorkPilotException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please check the logs."},
    )

origins = [
    "http://localhost:3000",
]

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

class CatchAllExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={"detail": "An internal server error occurred (middleware level)."},
            )

app.add_middleware(CatchAllExceptionsMiddleware)
app.add_middleware(TenantMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"http://.*\.localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers

app.include_router(auth_router)
app.include_router(invitation_router)
app.include_router(invitation_internal_router)


@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "debug": settings.DEBUG,
    }
