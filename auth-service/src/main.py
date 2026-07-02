from fastapi import FastAPI

from src.core.config import settings

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "debug": settings.DEBUG,
    }