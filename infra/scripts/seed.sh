#!/usr/bin/env bash
# Seed taxonomy data (run from repo root)
cd apps/api && uv run python -m app.db.seed
