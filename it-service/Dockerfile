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
COPY it-service/pyproject.toml it-service/README.md* /app/it-service/

WORKDIR /app/it-service
RUN uv sync --frozen --no-dev

# ---------------------------------------
# Development Stage
# ---------------------------------------
FROM base AS dev

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* /app/
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY it-service/pyproject.toml it-service/README.md* /app/it-service/

WORKDIR /app/it-service
RUN uv sync --frozen

COPY it-service /app/it-service

ENV PYTHONPATH=/app/it-service/src
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.it_service.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------------------------------------
# Production Stage
# ---------------------------------------
FROM base AS prod

COPY --from=builder /app/it-service/.venv /app/it-service/.venv
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY it-service /app/it-service

WORKDIR /app/it-service

ENV PATH="/app/it-service/.venv/bin:$PATH"
ENV PYTHONPATH=/app/it-service/src

EXPOSE 8000
CMD ["uvicorn", "src.it_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
