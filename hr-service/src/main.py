from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from shared_infrastructure.core.config import settings
from shared_infrastructure.core.exceptions import WorkPilotException
from src.modules.attendance.router import router as attendance_router
from src.modules.employee.router import router as employee_router
from src.modules.employee.internal_router import internal_router
from src.modules.leave.router import (
    employee_leave_router,
    holiday_router,
    leave_balance_router,
    leave_calendar_router,
    leave_report_router,
    leave_type_router,
)
from src.modules.leave.router import (
    router as leave_router,
    leave_request_router,
)
from src.modules.organization.router import router as organization_router
from src.modules.policies.router import (
    attendance_policy_router,
    holiday_policy_router,
    leave_policy_router,
    probation_policy_router,
    shift_policy_router,
)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    from shared_infrastructure.publisher import broker
    await broker.start()
    yield
    await broker.close()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)


# =====================================================
# Global Exception Handler
# =====================================================

@app.exception_handler(WorkPilotException)
async def workpilot_exception_handler(
    request: Request,
    exc: WorkPilotException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please check the logs.",
        },
    )


# =====================================================
# CORS
# =====================================================

origins = [
    "http://localhost:3000",
    "http://google.localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"http://[a-zA-Z0-9-]+\.localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Routers
# =====================================================

app.include_router(employee_router)
app.include_router(internal_router)
app.include_router(organization_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(leave_type_router)
app.include_router(employee_leave_router)
app.include_router(leave_request_router)
app.include_router(leave_balance_router)
app.include_router(leave_report_router)
app.include_router(leave_calendar_router)
app.include_router(holiday_router)
app.include_router(leave_policy_router)
app.include_router(attendance_policy_router)
app.include_router(shift_policy_router)
app.include_router(holiday_policy_router)
app.include_router(probation_policy_router)

# =====================================================
# Root Endpoint
# =====================================================

@app.get("/")
def home():
    return {
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "status": "Running",
    }


# =====================================================
# Health Check
# =====================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }