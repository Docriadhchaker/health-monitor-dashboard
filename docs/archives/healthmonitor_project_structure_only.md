# Project Structure

## 1. Purpose

This document defines the recommended repository and folder structure for the HealthMonitor MVP codebase.

It is intended to guide implementation in Cursor and ensure that the project is organized around the confirmed MVP architecture:
- React + TypeScript + Vite frontend
- FastAPI + Python backend
- PostgreSQL + PostGIS database
- Redis + Celery worker system
- Separate ingestion and enrichment pipeline
- Five MVP data layers:
  1. Public Health / Surveillance
  2. Guidelines
  3. Scientific Literature
  4. Preprints
  5. Pharmacovigilance

This document covers structure only. It does not redefine product requirements, styling rules, or database schema details.

---

## 2. Structural Principles

The repository should follow these principles:

1. **Single monorepo for the MVP**
   - Frontend, backend, workers, shared contracts, docs, and infrastructure should live in one repository.

2. **Clear runtime separation**
   - The user-facing API, background workers, and ingestion jobs must be structurally separated.

3. **Separation of raw ingestion and canonical application data**
   - Raw source acquisition, normalization, summarization, and canonical event publication should not be mixed in a single module.

4. **Shared contracts where useful**
   - Cross-service event payloads, enums, and API contracts should be documented in one place.

5. **Testability by default**
   - Frontend and backend test folders must be first-class parts of the structure.

6. **Environment-safe configuration**
   - Credentials and API keys must never be stored in tracked JSON config files.
   - Secrets must be injected via environment variables.

---

## 3. Recommended Repository Layout

```text
healthmonitor/
├─ README.md
├─ .gitignore
├─ .editorconfig
├─ .env.example
├─ docker-compose.yml
├─ Makefile
├─ package.json
├─ pnpm-workspace.yaml
│
├─ apps/
│  ├─ web/
│  ├─ api/
│  └─ worker/
│
├─ packages/
│  ├─ shared-types/
│  ├─ shared-config/
│  └─ ui/
│
├─ ingestion/
│  ├─ sources/
│  ├─ normalization/
│  ├─ enrichment/
│  ├─ deduplication/
│  └─ jobs/
│
├─ infra/
│  ├─ docker/
│  ├─ scripts/
│  ├─ deployment/
│  └─ monitoring/
│
├─ docs/
│  ├─ product/
│  ├─ architecture/
│  ├─ api/
│  └─ operations/
│
├─ tests/
│  ├─ e2e/
│  ├─ integration/
│  └─ fixtures/
│
└─ notebooks/
   ├─ exploration/
   └─ experiments/
```

---

## 4. Top-Level Directory Responsibilities

### 4.1 `apps/`
Contains all runtime applications used by the MVP.

- `web/` = user-facing frontend
- `api/` = backend HTTP API
- `worker/` = asynchronous jobs and scheduled tasks

### 4.2 `packages/`
Contains reusable shared packages.

- `shared-types/` = shared enums, DTOs, and API payload contracts
- `shared-config/` = shared configuration constants and validation helpers
- `ui/` = optional shared UI primitives if needed

### 4.3 `ingestion/`
Contains the data acquisition and transformation pipeline.

This folder is separate from `apps/api` because ingestion is not the same concern as query-serving.

### 4.4 `infra/`
Contains infrastructure, containerization, deployment, and operational scripts.

### 4.5 `docs/`
Contains product-facing and engineering-facing documentation.

### 4.6 `tests/`
Contains system-level and cross-app test assets.

### 4.7 `notebooks/`
Contains exploratory analysis only.

This folder must never be treated as part of the production runtime.

---

## 5. Frontend Structure

Frontend location:

```text
apps/web/
```

Recommended structure:

```text
apps/web/
├─ public/
├─ src/
│  ├─ app/
│  │  ├─ router/
│  │  ├─ providers/
│  │  └─ layouts/
│  │
│  ├─ components/
│  │  ├─ map/
│  │  ├─ event-card/
│  │  ├─ filters/
│  │  ├─ panels/
│  │  ├─ badges/
│  │  └─ common/
│  │
│  ├─ features/
│  │  ├─ map-explorer/
│  │  ├─ event-details/
│  │  ├─ layer-controls/
│  │  ├─ search/
│  │  ├─ translation/
│  │  └─ region-selection/
│  │
│  ├─ hooks/
│  ├─ lib/
│  ├─ services/
│  ├─ store/
│  ├─ styles/
│  ├─ types/
│  ├─ utils/
│  ├─ i18n/
│  └─ main.tsx
├─ tests/
├─ vite.config.ts
├─ tsconfig.json
└─ package.json
```

### 5.1 Frontend folder intent

- `app/` = root application wiring, providers, layout, and routing
- `components/` = reusable UI components
- `features/` = feature-oriented grouping for product behavior
- `services/` = API calls and data access wrappers
- `store/` = frontend state management
- `i18n/` = language resources and translation configuration
- `styles/` = global styles and design tokens
- `tests/` = frontend unit/component tests

### 5.2 Frontend feature modules expected for MVP

At minimum, the frontend should include dedicated feature modules for:
- world map rendering
- marker clustering
- layer toggles
- region and country filters
- time-window filter
- compact event card
- source verification flow
- English/French summary toggle
- loading, empty, and degraded states

---

## 6. Backend API Structure

Backend location:

```text
apps/api/
```

Recommended structure:

```text
apps/api/
├─ app/
│  ├─ api/
│  │  └─ v1/
│  │     ├─ endpoints/
│  │     └─ router.py
│  │
│  ├─ core/
│  │  ├─ config.py
│  │  ├─ logging.py
│  │  ├─ security.py
│  │  └─ constants.py
│  │
│  ├─ db/
│  │  ├─ session.py
│  │  ├─ base.py
│  │  └─ migrations/
│  │
│  ├─ models/
│  ├─ schemas/
│  ├─ repositories/
│  ├─ services/
│  ├─ integrations/
│  ├─ dependencies/
│  └─ main.py
│
├─ tests/
├─ alembic.ini
├─ pyproject.toml
└─ package_metadata.md
```

### 6.1 Backend folder intent

- `api/v1/endpoints/` = HTTP route handlers grouped by domain
- `core/` = app configuration and cross-cutting concerns
- `db/` = database initialization and migrations
- `models/` = ORM models
- `schemas/` = request/response validation models
- `repositories/` = database access layer
- `services/` = business logic layer
- `integrations/` = third-party service wrappers
- `dependencies/` = shared dependency injection helpers

### 6.2 Expected backend endpoint domains for MVP

At minimum, endpoint modules should be organized around:
- `events`
- `layers`
- `sources`
- `regions`
- `search`
- `translations`
- `health`

Possible layout:

```text
apps/api/app/api/v1/endpoints/
├─ events.py
├─ layers.py
├─ sources.py
├─ regions.py
├─ search.py
├─ translations.py
└─ health.py
```

---

## 7. Worker Structure

Worker location:

```text
apps/worker/
```

Recommended structure:

```text
apps/worker/
├─ worker/
│  ├─ celery_app.py
│  ├─ schedules.py
│  ├─ tasks/
│  │  ├─ ingest.py
│  │  ├─ normalize.py
│  │  ├─ geocode.py
│  │  ├─ summarize.py
│  │  ├─ translate.py
│  │  ├─ deduplicate.py
│  │  └─ publish.py
│  ├─ services/
│  └─ utils/
├─ tests/
└─ pyproject.toml
```

### 7.1 Worker responsibilities

The worker app is responsible for background and scheduled processing only.

It should handle:
- polling feeds and APIs
- normalization jobs
- geocoding jobs
- AI summarization jobs
- translation jobs
- deduplication jobs
- canonical event publication jobs

The worker should not expose public API routes.

---

## 8. Ingestion Pipeline Structure

Pipeline location:

```text
ingestion/
```

Recommended structure:

```text
ingestion/
├─ sources/
│  ├─ pubmed/
│  ├─ europe_pmc/
│  ├─ medrxiv/
│  ├─ who_rss/
│  ├─ ecdc_rss/
│  └─ openfda/
│
├─ normalization/
│  ├─ parsers/
│  ├─ mappers/
│  └─ validators/
│
├─ enrichment/
│  ├─ geo/
│  ├─ ai_summary/
│  ├─ translation/
│  └─ tagging/
│
├─ deduplication/
│  ├─ rules/
│  ├─ matching/
│  └─ canonicalization/
│
├─ jobs/
│  ├─ run_ingestion.py
│  ├─ run_backfill.py
│  └─ run_reprocessing.py
│
└─ tests/
```

### 8.1 Ingestion responsibilities

This part of the repository is responsible for:
- source-specific retrieval
- raw payload parsing
- normalized record creation
- location extraction support
- topic/specialty tagging support
- canonicalization inputs for downstream publishing

### 8.2 Source adapters expected for MVP

The MVP should have dedicated source adapters for:
- PubMed
- Europe PMC
- medRxiv / bioRxiv
- WHO RSS
- ECDC RSS
- openFDA

Additional source adapters may be added later, but not mixed into the MVP structure prematurely.

---

## 9. Shared Packages Structure

Shared packages location:

```text
packages/
```

Recommended structure:

```text
packages/
├─ shared-types/
│  ├─ src/
│  │  ├─ enums/
│  │  ├─ event/
│  │  ├─ source/
│  │  ├─ layer/
│  │  └─ api/
│  └─ package.json
│
├─ shared-config/
│  ├─ src/
│  │  ├─ constants/
│  │  ├─ layers/
│  │  └─ validation/
│  └─ package.json
│
└─ ui/
   ├─ src/
   │  ├─ badges/
   │  ├─ cards/
   │  ├─ buttons/
   │  └─ feedback/
   └─ package.json
```

### 9.1 What should be shared

The repository may share:
- event enums
- layer identifiers
- source-class identifiers
- trust-tier identifiers
- API payload contracts
- UI primitives if reuse becomes meaningful

Do not over-engineer shared packages in the first implementation.

---

## 10. Infrastructure Structure

Infrastructure location:

```text
infra/
```

Recommended structure:

```text
infra/
├─ docker/
│  ├─ api.Dockerfile
│  ├─ worker.Dockerfile
│  └─ web.Dockerfile
│
├─ scripts/
│  ├─ bootstrap.sh
│  ├─ dev-up.sh
│  ├─ lint.sh
│  ├─ test.sh
│  └─ seed.sh
│
├─ deployment/
│  ├─ web/
│  ├─ api/
│  └─ worker/
│
└─ monitoring/
   ├─ logging/
   ├─ metrics/
   └─ sentry/
```

### 10.1 Infrastructure expectations

The MVP repository should explicitly support:
- local development via Docker Compose
- separate service containers for web, api, worker, postgres, and redis
- deployment config separated by service
- scriptable setup for new developers
- basic monitoring and error tracking hooks

### 10.2 Secrets and configuration

Secrets must not be stored in tracked JSON files.

They must come from:
- `.env` files for local development
- environment variables in deployed environments
- managed secret stores in production if available

---

## 11. Documentation Structure

Documentation location:

```text
docs/
```

Recommended structure:

```text
docs/
├─ product/
│  ├─ PRD.md
│  ├─ user-flow.md
│  └─ styling-guidelines.md
│
├─ architecture/
│  ├─ technology-stack.md
│  ├─ project-structure.md
│  └─ database-schema.md
│
├─ api/
│  ├─ endpoints.md
│  └─ examples.md
│
└─ operations/
   ├─ local-setup.md
   ├─ deployment.md
   └─ ingestion-runbook.md
```

This ensures that Cursor and developers can navigate implementation guidance without mixing product and engineering concerns.

---

## 12. Testing Structure

Testing must exist at both application level and cross-system level.

Recommended structure:

```text
tests/
├─ e2e/
│  ├─ map-navigation/
│  ├─ filtering/
│  ├─ event-card/
│  └─ source-verification/
│
├─ integration/
│  ├─ ingestion/
│  ├─ api/
│  └─ worker/
│
└─ fixtures/
   ├─ sample-events/
   ├─ source-payloads/
   └─ geodata/
```

### 12.1 Expected coverage areas

At minimum, tests should cover:
- source ingestion parsing
- event normalization
- deduplication rules
- map filtering behavior
- event card rendering
- translation toggle behavior
- API response structure
- degraded source handling

---

## 13. Naming and Module Conventions

The repository should follow these conventions:

- Use **feature-oriented names** where possible
- Keep file and folder names lowercase with hyphen or underscore consistency per language norms
- Keep API versioning explicit
- Keep source adapters isolated by provider
- Keep event processing stages separate by folder
- Avoid generic folders like `misc/`, `helpers/`, or `temp/` in the core project

Examples:
- good: `map-explorer`, `event-card`, `source_class.py`, `pubmed_adapter.py`
- bad: `utils2`, `random`, `newfolder`, `service_final`

---

## 14. MVP Scope Boundaries for Structure

The structure should support the MVP only.

The following should **not** be treated as first-class runtime modules yet:
- user accounts
- persistent bookmarks
- notification center
- role-based workspaces
- real-time collaboration
- patient data integration
- FHIR or EHR connectors
- Elasticsearch
- social media ingestion
- YouTube live ingestion as a core pipeline module

These can be added later without destabilizing the initial structure.

---

## 15. Final Recommendation

The HealthMonitor MVP should be implemented as a **single monorepo with clearly separated web, API, worker, ingestion, infrastructure, documentation, and test boundaries**.

The structure must make these workflows obvious:
- ingest external health signals
- normalize and enrich them
- deduplicate and publish canonical events
- expose them through a clean API
- render them in a map-first frontend

A clean project structure is critical because this product depends on multiple pipelines, multiple source types, and multiple runtime roles. If the repository is poorly structured from the start, implementation quality and maintainability will degrade quickly.
