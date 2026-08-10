from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from shared_infrastructure.core.config import settings
from shared_infrastructure.core.exceptions import WorkPilotException


app = FastAPI(
    title="Analytics Service",
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
# Root Endpoint
# =====================================================

@app.get("/")
def home():
    return {
        "service": "Analytics Service",
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
