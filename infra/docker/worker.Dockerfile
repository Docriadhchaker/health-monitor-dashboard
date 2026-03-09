FROM python:3.12-slim

WORKDIR /app

RUN pip install uv
COPY apps/worker/pyproject.toml apps/worker/
COPY apps/api/pyproject.toml apps/api/
RUN cd apps/worker && uv sync --no-dev

COPY apps/worker/ apps/worker/
COPY apps/api/ apps/api/
COPY ingestion/ ingestion/

ENV PYTHONPATH=/app/apps/worker:/app/apps/api:/app
CMD ["uv", "run", "--project", "apps/worker", "celery", "-A", "worker.celery_app:app", "worker", "-l", "info"]
