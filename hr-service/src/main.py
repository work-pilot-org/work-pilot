from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.config import settings
from src.core.exceptions import WorkPilotException

from src.modules.employee.router import router as employee_router
from src.modules.organization.router import router as organization_router
from src.modules.attendance.router import router as attendance_router
from src.modules.leave.router import (
    router as leave_router,
    leave_type_router,
    employee_leave_router,
    leave_balance_router,
    leave_report_router,
    leave_calendar_router,
    holiday_router,
)



app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
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


# =====================================================
# CORS
# =====================================================

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


# =====================================================
# Routers
# =====================================================

app.include_router(employee_router)
app.include_router(organization_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(leave_type_router)
app.include_router(employee_leave_router)
app.include_router(leave_balance_router)
app.include_router(leave_report_router)
app.include_router(leave_calendar_router)
app.include_router(holiday_router)

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