# Technology Stack: HealthMonitor

## 1. Overview

This document defines the official technology stack for the HealthMonitor MVP. It is intended to guide implementation in Cursor and to remove ambiguity about primary tools, deployment assumptions, and service boundaries.

The stack is optimized for the following product requirements:
- Interactive global map with dense event visualization and mandatory clustering
- Reliable ingestion of health-related public data streams
- Metadata-rich filtering by layer, geography, trust tier, source class, and topic
- Short, neutral AI summaries with strict validation constraints
- English-first interface with French translation for UI labels and AI summaries
- MVP scale target of up to 10,000 active, queryable events with smooth interaction

## 2. Architecture Principles

The MVP architecture follows these principles:
- **Map-first performance:** frontend and backend choices must support geospatial filtering, clustering, and viewport-based loading.
- **Strict typing and schema control:** event data must be validated and normalized before storage and delivery.
- **Decoupled ingestion and enrichment:** source polling, parsing, geocoding, deduplication, summarization, and translation run asynchronously.
- **Traceability over automation:** every surfaced event must preserve the original source link, source title, timestamps, and classification metadata.
- **Low-complexity MVP:** prioritize a small number of proven technologies that Cursor can implement reliably.

## 3. Official MVP Stack Decisions

### 3.1 Frontend

| Category | Official Choice | Reason |
|---|---|---|
| UI Framework | **React 18** | Mature ecosystem for complex dashboards and component-driven UI |
| Language | **TypeScript** | Required for strict typing of events, filters, and API contracts |
| Build Tool | **Vite** | Fast local development and simple production builds |
| Mapping Library | **MapLibre GL JS** | WebGL rendering, clustering support, open-source, well suited to dense geospatial views |
| State / Server Cache | **TanStack Query** | Clean client-side data fetching, cache invalidation, and background refresh |
| Styling | **Tailwind CSS** | Fast implementation, consistent utility system, easy enforcement of design tokens |
| Internationalization | **i18next** | Stable multilingual UI support for English-first, French-enabled interface |
| Iconography | **Lucide React** | Clean, lightweight icon set suitable for clinical UI |

### 3.2 Backend API

| Category | Official Choice | Reason |
|---|---|---|
| API Framework | **FastAPI** | Strong performance, excellent developer experience, native OpenAPI generation |
| Language | **Python 3.12** | Best fit for ingestion, NLP/LLM integration, and data processing workflows |
| Validation | **Pydantic v2** | Strong runtime validation for strict event schemas |
| ORM / DB Layer | **SQLAlchemy 2.x** | Flexible relational modeling and integration with Postgres/PostGIS |
| Authentication | **None for MVP public read mode** | Reduces complexity for initial build; admin controls can be environment-protected |

### 3.3 Database and Search

| Category | Official Choice | Reason |
|---|---|---|
| Primary Database | **PostgreSQL 16** | Reliable relational core for normalized event and source metadata |
| Geospatial Extension | **PostGIS** | Required for bounding-box queries, region filters, and geospatial indexing |
| Text Search | **PostgreSQL Full-Text Search** | Sufficient for MVP keyword search |
| Fuzzy Matching | **pg_trgm** | Supports deduplication and approximate title matching |
| Cache / Broker | **Redis** | Shared cache plus task queue broker for workers |

### 3.4 Background Processing

| Category | Official Choice | Reason |
|---|---|---|
| Task Queue | **Celery** | Proven async job execution for ingestion and enrichment |
| Scheduler | **Celery Beat** | Periodic source polling and maintenance jobs |
| HTTP Client | **httpx** | Async-friendly source fetching |
| RSS Parsing | **feedparser** | Reliable RSS/Atom ingestion for official feeds |
| HTML Parsing | **BeautifulSoup4** | Fallback extraction when source metadata is incomplete |
| Geocoding | **GeoPy + Nominatim fallback** | Cost-effective MVP geocoding for textual locations |

### 3.5 AI and Translation Services

| Category | Official Choice | Reason |
|---|---|---|
| AI Summarization Provider | **OpenAI API** | Fastest path for constrained neutral summaries in MVP |
| Translation Provider | **DeepL API Pro** | Strong EN↔FR quality and glossary support for medical terminology |
| Summary Safety Layer | **Custom validation pass in Python** | Mandatory enforcement of prompt red lines and blocked wording |

### 3.6 Infrastructure and Deployment

| Category | Official Choice | Reason |
|---|---|---|
| Local Development | **Docker Compose** | Simple multi-service local environment for Cursor and developer onboarding |
| Frontend Hosting | **Vercel** | Fast deployment for React/Vite static frontend |
| API / Worker Hosting | **Railway** | Simple MVP deployment for FastAPI, Celery workers, and scheduled jobs |
| Managed Database | **Railway PostgreSQL** or equivalent managed Postgres with PostGIS | Reduces ops burden for MVP |
| Secrets Management | **Environment variables** | Sufficient for MVP deployment model |
| Error Monitoring | **Sentry** | Minimal production observability for frontend and backend |
| Logging | **Structured JSON logs** | Easier debugging of ingestion, API, and worker pipelines |

## 4. Service Boundaries

The MVP should be implemented as four runtime services:

1. **Frontend App**
   - React/Vite application
   - Map UI, filters, event cards, translation toggle, region presets

2. **Backend API**
   - FastAPI service
   - Filtered event retrieval, source metadata endpoints, region summary endpoints

3. **Worker Service**
   - Celery workers
   - Ingestion, parsing, classification, geocoding, deduplication, summarization, translation

4. **Redis + PostgreSQL**
   - Shared infrastructure services
   - Queue broker, cache, relational store, geospatial queries

## 5. MVP Source Ingestion Stack

The official MVP ingestion stack is:
- **NCBI PubMed (E-utilities)**
- **Europe PMC REST API**
- **medRxiv / bioRxiv API**
- **WHO RSS feeds**
- **ECDC RSS feeds**

The following source is **out of MVP scope and deferred to Phase 2**:
- **ClinicalTrials.gov API v2**

## 6. Data Processing Pipeline

Each event should pass through the following pipeline:

1. Source fetch
2. Parse and normalize raw metadata
3. Assign source class and default trust tier
4. Extract or infer event type / layer
5. Geocode location if a geographic entity is present
6. Deduplicate against recent related items
7. Generate English AI summary
8. Validate summary against hard constraints
9. Translate summary to French
10. Store final event record and indexing metadata
11. Expose through API for map and filter views

## 7. Frontend Technical Requirements

The frontend implementation must support:
- Interactive world map with marker clustering
- Region presets: World, Americas, MENA, Europe, Asia, Africa, Oceania
- Country-level filtering
- Time window filtering: 24h, 7d, 30d
- Toggleable layers: Public Health, Guidelines, Literature, Pharmacovigilance, Preprints
- Overarching toggle for Official vs Non-Official sources
- Compact event cards with source class, trust tier, freshness, summary, tags, and source link
- English UI with French translation support
- Accessible interaction patterns conforming to WCAG 2.2 AA

## 8. Backend Technical Requirements

The backend must support:
- Bounding-box and region-based geospatial queries
- Layer filtering
- Source class and trust tier filtering
- Topic and specialty tag filtering
- Date-range filtering
- Keyword search
- Cluster-friendly event retrieval
- Region summary aggregation
- Source traceability fields on every event response

## 9. Performance Targets

The stack must be able to support the following MVP performance targets:
- **10,000 active queryable events** in the recent indexed pool
- Smooth interaction through clustering and viewport-based loading
- Normally fewer than **1,000 unclustered visible markers** at once
- Initial filtered map response in a few seconds under normal load
- High-priority official feed ingestion surfaced within roughly one hour of publication when source latency allows

## 10. Security and Compliance Notes

This MVP does **not** manage patient data, EHR data, or direct clinical records.
Therefore, the stack is optimized for public and licensed information ingestion rather than protected health data workflows.

Even so, the system must still preserve:
- source traceability
- audit-friendly timestamps
- controlled secret handling
- safe logging practices that avoid storing unnecessary raw payloads from third-party services

## 11. Development Environment

The repository should support a one-command local startup using Docker Compose with at least:
- `frontend`
- `api`
- `worker`
- `redis`
- `postgres`

Recommended environment variables:
- `DATABASE_URL`
- `REDIS_URL`
- `OPENAI_API_KEY`
- `DEEPL_API_KEY`
- `APP_ENV`
- `SENTRY_DSN`

## 12. Deferred Technical Decisions (Phase 2+)

The following are intentionally deferred:
- User accounts and RBAC
- Saved searches and alerts
- ClinicalTrials.gov ingestion
- YouTube live ingestion and embedding workflows
- Advanced vector search or dedicated search engine
- Fine-grained province/city map analytics
- Custom drawn map regions
- Multi-provider LLM routing
- Full enterprise deployment architecture (Kubernetes, private VPC, etc.)

## 13. Final Stack Summary

**Frontend:** React + TypeScript + Vite + MapLibre GL JS + Tailwind CSS + TanStack Query + i18next  
**Backend:** Python 3.12 + FastAPI + Pydantic v2 + SQLAlchemy 2.x  
**Database:** PostgreSQL 16 + PostGIS + pg_trgm  
**Async / Cache:** Redis + Celery + Celery Beat  
**Ingestion:** httpx + feedparser + BeautifulSoup4 + GeoPy  
**AI / Translation:** OpenAI API + DeepL API Pro  
**Infra:** Docker Compose + Vercel + Railway + Sentry
