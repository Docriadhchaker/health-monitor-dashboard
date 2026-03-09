# HealthMonitor MVP — Plan d’implémentation

## 1. Résumés des six documents de spécification

### 1.1 PRD (Product Requirements Document)
- **Produit** : tableau de bord d’intelligence santé mondial en temps réel pour professionnels de santé.
- **Interface** : carte mondiale centrale, panneau gauche (couches, filtres, régions), cartes d’événements compactes.
- **5 couches MVP** : Public Health / Surveillance, Guidelines, Literature, Pharmacovigilance, Preprints.
- **Filtres** : région (World, Americas, MENA, Europe, Asia, Africa, Oceania), pays, fenêtre temporelle (24h, 7d, 30d), couches, Official vs Non-Official, source class, trust tier, thème/spécialité.
- **Carte** : clustering obligatoire, marqueurs selon filtres actifs.
- **Carte d’événement** : titre, couche, source class, trust tier, fraîcheur, résumé IA (50–90 mots, neutre), tags, géographie, statut de preuve, date, lieu, source, lien original ; actions : Open Source, Copy Link, Save/Bookmark (ce dernier reporté en User Flow).
- **Résumés IA** : descriptifs, courts, neutres, sans recommandation clinique ; contraintes strictes (pas de « should », pas de conseil, pas de causalité non sourcée).
- **Langues** : anglais par défaut, français ; résumés traduits étiquetés ; titres sources en langue d’origine.
- **Données** : PubMed, Europe PMC, medRxiv/bioRxiv, WHO/ECDC, sources pharmacovigilance ; déduplication (titre, URL, thème/lieu/temps) ; cible ~10k événements requêtables.
- **Hors périmètre MVP** : dessin géographique personnalisé, analytics géo avancées, comptes utilisateur avancés, YouTube live, données patients.

### 1.2 Technology Stack
- **Frontend** : React 18, TypeScript, Vite, MapLibre GL JS, TanStack Query, Tailwind CSS, i18next, Lucide React.
- **Backend** : FastAPI, Python 3.12, Pydantic v2, SQLAlchemy 2.x ; pas d’auth pour le MVP (lecture publique).
- **Base de données** : PostgreSQL 16, PostGIS, recherche full-text + pg_trgm ; Redis (cache + broker).
- **Tâches asynchrones** : Celery, Celery Beat ; httpx, feedparser, BeautifulSoup4, GeoPy/Nominatim.
- **IA / traduction** : OpenAI (résumés), DeepL (EN↔FR) ; couche de validation custom en Python.
- **Infra** : Docker Compose (local), Vercel (frontend), Railway (API + workers + DB) ; variables d’environnement ; Sentry ; logs JSON.
- **Services** : 4 runtimes — Frontend, API, Worker, Redis+PostgreSQL.
- **Ingestion officielle MVP** : PubMed, Europe PMC, medRxiv/bioRxiv, WHO RSS, ECDC RSS (ClinicalTrials.gov en Phase 2).

### 1.3 Database Schema Design
- **Séparation** : enregistrements bruts (`raw_documents`) vs événements canoniques (`events`).
- **Tables principales** : `source_providers`, `source_feeds`, `ingestion_runs`, `raw_documents` ; `events`, `event_source_links`, `event_locations`, `event_translations` ; taxonomies (`layers`, `source_classes`, `trust_tiers`, `evidence_statuses`, `specialties`, `topics`, `organizations`, `jurisdictions`) ; tables de liaison (`event_topics`, `event_specialties`, `event_organizations`) ; `ai_processing_jobs`, `event_change_log`.
- **Événement** : `layer_id`, `title`, `summary_en`, `primary_provider_id`, `evidence_status_id`, `trust_tier_id`, `geographic_scope`, `country_code`, `region_code`, `location_name`, `location_point` (PostGIS GEOGRAPHY), `metadata_json`, etc. ; pas de champ « freshness » stocké (calculé à l’affichage).
- **Indexation** : GIST sur `location_point`, GIN full-text sur titre + résumé, trigram sur titre, B-tree sur filtres.
- **Couches** : PUB_HEALTH, GUIDELINES, LITERATURE, PREPRINTS, PHARMACOVIGILANCE.

### 1.4 User Flow
- **Parcours** : Charger la vue (carte, région, temps, couches) → Repérer et trier sur la carte → Consulter la carte d’événement compacte → Vérifier la source (Open Source).
- **État initial** : région World, 7 jours, les 5 couches actives, langue anglais.
- **Carte compacte** : identité (titre, couche, source class, trust tier, fraîcheur), résumé IA, tags de contexte, détails (date, lieu, source), actions Open Source, Copy Link, Translate ; **Save/Bookmark reporté**.
- **Résumé** : formule « what + where + when + according to whom » ; pas de recommandation.
- **Filtres** : région, pays, fenêtre temps, couches, Official vs Non-Official, source class, trust tier, thème, spécialité.
- **Français** : UI et résumé traduits ; résumé traduit étiqueté ; résumé anglais original accessible (toggle).
- **États** : chargement, vide, dégradé (sources partiellement indisponibles).

### 1.5 Project Structure
- **Monorepo** : `apps/` (web, api, worker), `packages/` (shared-types, shared-config, ui), `ingestion/` (sources, normalization, enrichment, deduplication, jobs), `infra/` (docker, scripts, deployment, monitoring), `docs/`, `tests/` (e2e, integration, fixtures), `notebooks/`.
- **Frontend** : `apps/web/` — `src/app/`, `components/` (map, event-card, filters, panels, badges, common), `features/` (map-explorer, event-details, layer-controls, search, translation, region-selection), hooks, lib, services, store, styles, types, utils, i18n.
- **API** : `apps/api/` — `app/api/v1/endpoints/` (events, layers, sources, regions, search, translations, health), core, db, models, schemas, repositories, services, integrations, dependencies.
- **Worker** : `apps/worker/` — Celery, tasks (ingest, normalize, geocode, summarize, translate, deduplicate, publish), services, utils.
- **Ingestion** : adapters par source (pubmed, europe_pmc, medrxiv, who_rss, ecdc_rss, openfda), normalization, enrichment, deduplication, jobs.
- **Secrets** : uniquement via variables d’environnement ; pas de JSON suivi.

### 1.6 Styling Guidelines
- **Principes** : lisibilité clinique, ton calme et professionnel, couleur jamais seule (forme, icônes, libellés), WCAG 2.2 AA.
- **Tokens** : couleurs (light/dark), typo (Inter), espacements, radius, ombres, motion, z-index ; couleurs sémantiques par couche/source.
- **Layout** : rail gauche 320–360 px, carte centrale, carte d’événement 360–440 px, barre haute 56 px.
- **Composants** : carte (surface élevée, radius 14px), ordre de lecture (titre → meta → résumé → chips → détails → actions), marqueurs par forme/couleur (officiel=bleu cercle, littérature=vert cercle, preprint=ambre losange, pharmacovigilance=triangle rouge/ambre, etc.), clusters 28–48 px.
- **Implémentation** : Tailwind, variables CSS, variantes sémantiques.

---

## 2. Contradictions ou écarts identifiés

| Sujet | Document A | Document B | Résolution proposée |
|-------|-------------|-------------|----------------------|
| **Trust tier** | User Flow : "High, **Medium**, Exploratory" | DB : HIGH, **MODERATE**, EXPLORATORY | Conserver le schéma DB (MODERATE) ; afficher "Medium" en UI si besoin. |
| **Save/Bookmark** | PRD 4.5 : "Core actions … Save/Bookmark" | User Flow 4.1 : "Save/Bookmark is **deferred** from MVP" | Suivre User Flow : ne pas implémenter Save/Bookmark en MVP. |
| **openFDA** | Tech Stack §5 : liste d’ingestion sans openFDA (PubMed, Europe PMC, medRxiv, WHO, ECDC) | Project Structure 8.2 : "openFDA" dans les adapters attendus | PRD 5.1 inclut "pharmacovigilance and drug-safety sources". **Inclure openFDA** dans le pipeline MVP comme dans Project Structure. |
| **Ordre des couches (4 et 5)** | User Flow 6.1 : "… Literature, **Pharmacovigilance**, **Preprints**" | PRD/DB : L-PHV puis L-PRE (Pharmacovigilance puis Preprints) | Aligner sur le schéma : 1 PUB, 2 GUI, 3 LIT, 4 PHV, 5 PRE. |

Aucune autre contradiction bloquante ; les docs sont alignés sur l’architecture (pas de Node, pas d’Elasticsearch, 5 couches, pipeline raw → canonical).

---

## 3. Plan d’implémentation par phases

| Phase | Objectif | Livrables principaux |
|-------|-----------|----------------------|
| **1. Fondations** | Repo, infra locale, schéma DB, contrats partagés | Scaffold monorepo, Docker Compose (postgres, redis, api, worker, web), migrations Alembic, seed taxonomies, packages shared-types / shared-config (stubs) |
| **2. Backend cœur** | API opérationnelle, modèles, dépôts | FastAPI app, config, session DB, modèles SQLAlchemy, schémas Pydantic, endpoints v1 : health, layers, sources, events (stub), regions (stub) |
| **3. Pipeline d’ingestion** | Données brutes → `raw_documents` | Adapters (WHO RSS, ECDC RSS, PubMed, Europe PMC, medRxiv, openFDA), parsing/normalisation, écriture `raw_documents` + `ingestion_runs`, tâches Celery d’ingestion |
| **4. Enrichissement et publication** | Événements canoniques | Géocodage, déduplication, résumé IA (OpenAI) + validation, traduction (DeepL), création/MAJ `events` + `event_source_links` / `event_translations`, planning Beat |
| **5. API complète** | Filtrage et recherche | Endpoints events (bbox, couche, temps, source, trust, pays, région), event by id, search (full-text), region summary, translations |
| **6. Frontend** | Carte, filtres, carte d’événement | App Vite+React+TS, MapLibre + clustering, rail gauche (couches, filtres), carte d’événement, i18n EN/FR, tokens (light/dark), états chargement/vide/dégradé |
| **7. Finalisation** | Qualité et déploiement | Tests E2E (map, filtres, carte, vérification source), docs (setup, API, runbook ingestion), config déploiement (Vercel, Railway), Sentry |

---

## 4. Liste de tâches par domaine

### Frontend
- Scaffold `apps/web` (Vite, React, TypeScript, Tailwind, i18next, TanStack Query).
- Layout : rail gauche, zone carte, barre haute (langue/thème/recherche).
- Carte : MapLibre, marqueurs, clustering par densité/zoom.
- Filtres : couches, région, fenêtre temps, pays, Official/Non-Official, source class, trust tier, thème, spécialité.
- Composant carte d’événement (structure, ordre de lecture, tokens).
- Overlay/drawer carte d’événement (carte restant visible).
- Actions : Open Source, Copy Link ; toggle traduction résumé.
- États : chargement, vide, dégradé.
- Tokens design (light/dark) et variantes couches/marqueurs.
- Accessibilité : focus, contraste, cibles 24px, non-color-only.

### Backend
- Scaffold `apps/api` (FastAPI, pyproject.toml).
- Core : config (pydantic-settings), logging, security (stub), constantes.
- DB : session, base, Alembic, modèles pour toutes les tables du schéma.
- Schémas Pydantic : events, layers, sources, filtres, régions, search, translations.
- Repositories : events, layers, sources, regions.
- Endpoints v1 : health, layers, sources, events (liste + by id), regions, search, translations.
- CORS, préfixe /api/v1.

### Database
- PostgreSQL 16 + PostGIS activé.
- Migration initiale : toutes les tables, contraintes, index (GIST, GIN, B-tree, trigram).
- Données de seed : layers, source_classes, trust_tiers, evidence_statuses (optionnel : specialties, topics).

### Pipeline d’ingestion
- Structure `ingestion/sources` (who_rss, ecdc_rss, pubmed, europe_pmc, medrxiv, openfda).
- Chaque adapter : fetch, parse, sortie normalisée vers raw_documents.
- Normalisation : parsers, mappers, validators ; écriture `raw_documents`, mise à jour `ingestion_runs`.
- Point d’entrée `ingestion/jobs/run_ingestion.py` (appelable par worker).

### Workers / tâches de fond
- App Celery (broker Redis), connexion DB partagée avec l’API.
- Tâches : ingest (par feed), normalize, geocode, summarize, translate, deduplicate, publish.
- Celery Beat : planification ingestion périodique par feed.
- Dockerfile worker ; variables OPENAI_API_KEY, DEEPL_API_KEY.

### Infrastructure / config
- `docker-compose.yml` : services postgres (PostGIS), redis, api, worker, web.
- `.env.example` : DATABASE_URL, REDIS_URL, OPENAI_API_KEY, DEEPL_API_KEY, APP_ENV, SENTRY_DSN.
- Makefile : dev-up, test, lint, seed.
- `infra/docker` : Dockerfiles api, worker, web.
- `infra/scripts` : bootstrap, dev-up, seed (appels cohérents avec le monorepo).
- Packages : shared-types, shared-config (package.json, exports minimaux).

---

## 5. Fichiers à créer en premier (ordre suggéré)

1. **Racine** : `README.md`, `.gitignore`, `.editorconfig`, `.env.example`, `docker-compose.yml`, `Makefile`, `package.json`, `pnpm-workspace.yaml`
2. **DB / API** : `apps/api/pyproject.toml`, `apps/api/app/main.py`, `apps/api/app/core/config.py`, `apps/api/app/db/session.py`, `apps/api/app/db/base.py`, `alembic.ini` + `apps/api/app/db/migrations/versions/` (migration initiale)
3. **Modèles** : `apps/api/app/models/` (fichiers par entité : layer, source_provider, source_feed, event, raw_document, etc.)
4. **Schémas** : `apps/api/app/schemas/` (event, layer, filter params)
5. **Endpoints** : `apps/api/app/api/v1/endpoints/health.py`, `layers.py`, `events.py` (stub)
6. **Worker** : `apps/worker/pyproject.toml`, `apps/worker/worker/celery_app.py`, `apps/worker/worker/tasks/ingest.py` (stub)
7. **Ingestion** : `ingestion/sources/who_rss/`, `ingestion/sources/ecdc_rss/` (stubs), `ingestion/normalization/`, `ingestion/jobs/run_ingestion.py`
8. **Frontend** : `apps/web/package.json`, `apps/web/vite.config.ts`, `apps/web/tsconfig.json`, `apps/web/index.html`, `apps/web/src/main.tsx`, `apps/web/src/App.tsx`, structure dossiers `app/`, `components/`, `features/`, `styles/`
9. **Packages** : `packages/shared-types/package.json` + `src/`, `packages/shared-config/package.json` + `src/`
10. **Infra** : `infra/docker/api.Dockerfile`, `infra/docker/worker.Dockerfile`, `infra/docker/web.Dockerfile`, `infra/scripts/dev-up.sh`, `infra/scripts/seed.sh`
11. **Docs** : `docs/product/`, `docs/architecture/`, `docs/api/`, `docs/operations/` (fichiers .md de base)
12. **Tests** : `tests/e2e/`, `tests/integration/`, `tests/fixtures/` (structure + 1 test ou fixture exemple)

Ce document sert de référence pour l’implémentation sans dévier du MVP ni introduire Elasticsearch ou un backend Node.

---

## 6. Arborescence proposée (scaffold créé)

```text
Health monitor dashboard/
├── .cursor/rules/health-monitor-project.mdc
├── .editorconfig
├── .env.example
├── .gitignore
├── README.md
├── docker-compose.yml
├── Makefile
├── package.json
├── pnpm-workspace.yaml
│
├── apps/
│   ├── api/
│   │   ├── alembic.ini
│   │   ├── pyproject.toml
│   │   └── app/
│   │       ├── main.py
│   │       ├── api/v1/router.py
│   │       ├── api/v1/endpoints/ (health, layers, events, sources, regions, search, translations)
│   │       ├── core/config.py
│   │       ├── db/ (session, base, migrations, seed.py)
│   │       ├── models/
│   │       ├── schemas/
│   │       └── repositories/
│   ├── web/
│   │   ├── package.json, vite.config.ts, tsconfig.json, index.html
│   │   ├── tailwind.config.js, postcss.config.js
│   │   └── src/
│   │       ├── main.tsx, App.tsx
│   │       ├── app/router/
│   │       ├── components/ (map, event-card, filters)
│   │       ├── features/map-explorer/
│   │       ├── styles/global.css
│   │       └── i18n/
│   └── worker/
│       ├── pyproject.toml
│       └── worker/
│           ├── celery_app.py
│           ├── schedules.py
│           └── tasks/ (ingest.py, …)
│
├── packages/
│   ├── shared-types/ (enums/layers, event/types)
│   ├── shared-config/ (REGION_PRESETS, TIME_WINDOWS)
│   └── ui/
│
├── ingestion/
│   ├── sources/ (who_rss, ecdc_rss, pubmed, europe_pmc, medrxiv, openfda)
│   ├── normalization/
│   ├── enrichment/
│   ├── deduplication/
│   └── jobs/run_ingestion.py
│
├── infra/
│   ├── docker/ (api.Dockerfile, worker.Dockerfile, web.Dockerfile)
│   └── scripts/ (bootstrap.sh, dev-up.sh, seed.sh)
│
├── docs/
│   ├── product/ (PRD, user-flow, styling-guidelines)
│   ├── architecture/ (technology-stack, project-structure, database-schema, implementation-plan)
│   ├── api/ (endpoints)
│   └── operations/ (local-setup, deployment, ingestion-runbook)
│
├── tests/
│   ├── e2e/map-navigation/
│   ├── integration/api/
│   └── fixtures/
│
└── notebooks/ (exploration, experiments)
```

---

## 7. Fichiers à créer en priorité (ordre recommandé)

1. **Racine** : README.md, .gitignore, .editorconfig, .env.example, docker-compose.yml, Makefile, package.json, pnpm-workspace.yaml  
2. **API / DB** : apps/api/pyproject.toml, app/main.py, app/core/config.py, app/db/session.py, app/db/base.py, alembic.ini + première migration (schéma complet)  
3. **Modèles** : apps/api/app/models/ (layer, source_provider, source_feed, event, raw_document, taxonomies, jointures)  
4. **Schémas** : apps/api/app/schemas/ (event, layer, filter params, region summary)  
5. **Endpoints** : health, layers, events (liste + by id), sources, regions, search, translations  
6. **Worker** : apps/worker/pyproject.toml, worker/celery_app.py, worker/tasks/ingest.py (puis normalize, geocode, summarize, translate, deduplicate, publish)  
7. **Ingestion** : ingestion/sources/who_rss, ecdc_rss (implémentation), puis pubmed, europe_pmc, medrxiv, openfda ; normalization ; jobs/run_ingestion.py  
8. **Frontend** : apps/web (Vite, React, TS, Tailwind), layout (rail + carte + barre), carte MapLibre + clustering, filtres, carte d’événement, i18n, tokens  
9. **Packages** : shared-types, shared-config (déjà en place en minimal)  
10. **Infra** : Dockerfiles, scripts (déjà en place)  
11. **Docs** : déjà en place ; mettre à jour au fil de l’eau  
12. **Tests** : tests/e2e, tests/integration, tests/fixtures (un premier test ou fixture dès que possible)
