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
    "http://apple.localhost:3000",
    "http://postman.localhost:3000",
    "http://benz.localhost:3000",
    "http://car.localhost:3000",
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
app.add_middleware(TenantMiddleware)

# Include Routers
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "debug": settings.DEBUG,
    }
