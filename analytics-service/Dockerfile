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
COPY analytics-service/pyproject.toml analytics-service/README.md* /app/analytics-service/

WORKDIR /app/analytics-service
RUN uv sync --frozen --no-dev

# ---------------------------------------
# Development Stage
# ---------------------------------------
FROM base AS dev

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* /app/
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY analytics-service/pyproject.toml analytics-service/README.md* /app/analytics-service/

WORKDIR /app/analytics-service
RUN uv sync --frozen

COPY analytics-service /app/analytics-service

ENV PYTHONPATH=/app/analytics-service/src
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------------------------------------
# Production Stage
# ---------------------------------------
FROM base AS prod

COPY --from=builder /app/analytics-service/.venv /app/analytics-service/.venv
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY analytics-service /app/analytics-service

WORKDIR /app/analytics-service

ENV PATH="/app/analytics-service/.venv/bin:$PATH"
ENV PYTHONPATH=/app/analytics-service/src

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
