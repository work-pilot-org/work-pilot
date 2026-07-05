from fastapi import FastAPI

from src.core.config import settings
from src.modules.auth.router import router as auth_router

app = FastAPI(
    title=settings.APP_NAME,
)

# Include Routers
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "debug": settings.DEBUG,
    }