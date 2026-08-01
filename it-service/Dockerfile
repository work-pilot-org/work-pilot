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

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock* README.md* ./

# Create a virtual environment and sync production dependencies
RUN uv sync --frozen --no-dev

# ---------------------------------------
# Development Stage
# ---------------------------------------
FROM base AS dev

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* README.md* ./
RUN uv sync --frozen

# Copy application source code
COPY . .



EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.it_service.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------------------------------------
# Production Stage
# ---------------------------------------
FROM base AS prod

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application source code
COPY . .

# Ensure the virtual environment is used
ENV PATH="/app/.venv/bin:$PATH"


EXPOSE 8000
CMD ["uvicorn", "src.it_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
