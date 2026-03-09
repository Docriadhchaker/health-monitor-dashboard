#!/usr/bin/env bash
# Bootstrap local dev: deps, env, migrations (run from repo root)
set -e
echo "HealthMonitor bootstrap: ensure .env exists and deps installed"
test -f .env || cp .env.example .env
cd apps/api && uv sync && cd ../..
cd apps/worker && uv sync && cd ../..
cd apps/web && pnpm install && cd ../..
