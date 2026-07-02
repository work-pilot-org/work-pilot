from fastapi import FastAPI

app = FastAPI(title="WorkPilot Auth Service")


@app.get("/")
def root():
    return {"message": "Auth Service Running"}
