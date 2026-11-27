# WorkPilot Notification Service

This service provides centralized notification logging and delivery routing (e.g., SendGrid integration) for the WorkPilot ecosystem.

## Environment Setup
Copy the template configuration file:
```bash
cp .env.example .env
```

## Running Locally
Start the FastAPI development server:
```bash
uv run uvicorn src.notification_service.main:app --host 0.0.0.0 --port 8000 --reload
```

## Running Tests
Execute the unit and integration test suite:
```bash
uv run pytest
```
