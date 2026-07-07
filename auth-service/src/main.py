from fastapi import FastAPI

from src.core.config import settings
from src.modules.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Middleware
from src.core.middleware import TenantMiddleware
app.add_middleware(TenantMiddleware)

# Include Routers
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "debug": settings.DEBUG,
    }
