# Health Monitor Dashboard (Prototype)

A prototype dashboard that aggregates public health signals (WHO, ECDC, etc.) and displays them on a global map.

## Features

- Global map with event clustering
- RSS ingestion (WHO AFRO, ECDC)
- Time filtering (24h / 7d / 30d)
- Event list grouped by publication date
- Links to original sources
- Simple geolocation fallback for regional events

## Tech stack

- **Frontend:** React / MapLibre
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Ingestion:** RSS feeds (WHO, ECDC)

## Project structure

- **apps/api** — FastAPI backend and ingestion (RSS parsing, event promotion, API endpoints)
- **apps/web** — React frontend (map, filters, event cards)
- **Ingestion pipeline** — RSS processing and event promotion from raw feed items to canonical events

## How to run locally

**Backend:**

```bash
cd apps/api
uv run uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd apps/web
pnpm dev
```

## Data sources

- WHO RSS (AFRO featured news)
- ECDC RSS (news / press releases)

## Limitations

- RSS ingestion only (no full APIs yet)
- Geolocation fallback at region level
- Prototype-level UI/UX

## License

MIT
