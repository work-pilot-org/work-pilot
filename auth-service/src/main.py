from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.modules.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from src.core.exceptions import WorkPilotException

app = FastAPI(
    title=settings.APP_NAME,
)

@app.exception_handler(WorkPilotException)
async def workpilot_exception_handler(request: Request, exc: WorkPilotException):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"http://.*\.localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Middleware
from src.infrastructure.middleware.tenant_middleware import TenantMiddleware
from src.infrastructure.middleware.rate_limit_middleware import RateLimitMiddleware

# Rate limit: max 60 requests per 60 seconds per IP
app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)
app.add_middleware(TenantMiddleware)

# Include Routers
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "debug": settings.DEBUG,
    }
