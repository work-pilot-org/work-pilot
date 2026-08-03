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
COPY ai-service/pyproject.toml ai-service/README.md* /app/ai-service/

WORKDIR /app/ai-service
RUN uv sync --frozen --no-dev

# ---------------------------------------
# Development Stage
# ---------------------------------------
FROM base AS dev

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* /app/
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY ai-service/pyproject.toml ai-service/README.md* /app/ai-service/

WORKDIR /app/ai-service
RUN uv sync --frozen

COPY ai-service /app/ai-service

ENV PYTHONPATH=/app/ai-service/src
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------------------------------------
# Production Stage
# ---------------------------------------
FROM base AS prod

COPY --from=builder /app/ai-service/.venv /app/ai-service/.venv
COPY packages/shared-infrastructure /app/packages/shared-infrastructure
COPY ai-service /app/ai-service

WORKDIR /app/ai-service

ENV PATH="/app/ai-service/.venv/bin:$PATH"
ENV PYTHONPATH=/app/ai-service/src

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
