FROM python:3.13-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY pyproject.toml uv.lock* README.md ./

RUN pip install uv

RUN uv sync

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]