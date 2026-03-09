# HealthMonitor

Real-time global health intelligence dashboard for healthcare professionals.

## MVP Stack

- **Frontend:** React 18 + TypeScript + Vite + MapLibre GL JS + Tailwind CSS
- **Backend:** FastAPI + Python 3.12
- **Database:** PostgreSQL 16 + PostGIS
- **Cache/Queue:** Redis
- **Workers:** Celery + Celery Beat

## Repository structure

- `apps/web` — React frontend
- `apps/api` — FastAPI backend
- `apps/worker` — Celery workers
- `packages/` — shared-types, shared-config, ui
- `ingestion/` — source adapters, normalization, enrichment, deduplication
- `infra/` — Docker, scripts, deployment
- `docs/` — product, architecture, API, operations
- `tests/` — e2e, integration, fixtures

## Local development

1. Copy `.env.example` to `.env` and set secrets.
2. Run `make dev-up` (or `docker compose up -d`).
3. See `docs/operations/local-setup.md` for details.

## Documentation

Specifications and implementation plan:

- `docs/product/` — PRD, user flow, styling
- `docs/architecture/` — technology stack, project structure, database schema, implementation plan
- `docs/api/` — endpoints, examples
- `docs/operations/` — local setup, deployment, ingestion runbook
