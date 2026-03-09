.PHONY: dev-up dev-down migrate seed test lint bootstrap run-api run-worker run-web

dev-up:
	docker compose up -d postgres redis
	@echo "Then: make migrate && make seed"
	@echo "Then: make run-api (terminal 1), make run-worker (terminal 2), make run-web (terminal 3)"

dev-down:
	docker compose down

migrate:
	cd apps/api && uv run alembic upgrade head

seed:
	cd apps/api && uv run python -m app.db.seed

reset-events:
	cd apps/api && uv run python -m app.ingestion.reset_events_and_raw

ingest-who-ecdc:
	cd apps/api && uv run python -m app.ingestion.run_who_ecdc

run-api:
	cd apps/api && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-worker:
	cd apps/worker && uv run celery -A worker.celery_app:app worker -l info

run-web:
	cd apps/web && pnpm dev

test:
	cd apps/api && uv run pytest
	cd apps/worker && uv run pytest
	cd apps/web && pnpm test

lint:
	cd apps/api && uv run ruff check .
	cd apps/web && pnpm lint

bootstrap: dev-up
	@echo "Run: make migrate && make seed"
	@echo "Then start api, worker, web with make run-api, make run-worker, make run-web"
