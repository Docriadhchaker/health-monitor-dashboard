FROM python:3.12-slim

WORKDIR /app

RUN pip install uv
COPY apps/api/pyproject.toml apps/api/
RUN cd apps/api && uv sync --no-dev

COPY apps/api/ apps/api/
COPY ingestion/ ingestion/

ENV PYTHONPATH=/app/apps/api:/app
CMD ["uv", "run", "--project", "apps/api", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
