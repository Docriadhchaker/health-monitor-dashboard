# Local Setup

1. Clone the repository and `cd` into the root.
2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`, `DEEPL_API_KEY` when you implement summarization/translation (Phase 2).
3. Start infrastructure: `make dev-up` or `docker compose up -d postgres redis`.
4. Apply migrations: `make migrate` or `cd apps/api && uv run alembic upgrade head`.
5. Seed taxonomy: `make seed` or `cd apps/api && uv run python -m app.db.seed`.
6. Run API: `make run-api` or `cd apps/api && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
7. Run worker: `make run-worker` or `cd apps/worker && uv run celery -A worker.celery_app:app worker -l info`.
8. Run frontend: `make run-web` or `cd apps/web && pnpm dev` — open http://localhost:5173.

Requirements: Docker, Node 20+, pnpm, Python 3.12, uv (or pip).
