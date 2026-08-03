# ---------------------------------------
# Base Stage
# ---------------------------------------
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ---------------------------------------
# Builder Stage
# ---------------------------------------
FROM base AS builder

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY workflow-service/pyproject.toml workflow-service/README.md* /app/workflow-service/

WORKDIR /app/workflow-service
RUN uv sync --frozen --no-dev

# ---------------------------------------
# Development Stage
# ---------------------------------------
FROM base AS dev

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* /app/
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY workflow-service/pyproject.toml workflow-service/README.md* /app/workflow-service/

WORKDIR /app/workflow-service
RUN uv sync --frozen

COPY workflow-service /app/workflow-service

ENV PYTHONPATH=/app/workflow-service/src
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------------------------------------
# Production Stage
# ---------------------------------------
FROM base AS prod

COPY --from=builder /app/workflow-service/.venv /app/workflow-service/.venv
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY workflow-service /app/workflow-service

WORKDIR /app/workflow-service

ENV PATH="/app/workflow-service/.venv/bin:$PATH"
ENV PYTHONPATH=/app/workflow-service/src

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
