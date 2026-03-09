# Database Schema Design

## 1. Purpose

This document defines the database schema for **HealthMonitor**, a real-time global health intelligence dashboard for healthcare professionals.

The schema is designed to support:
- ingestion of heterogeneous public health and scientific sources,
- normalization of raw records into canonical events,
- geospatial querying for map visualization,
- filtering by layer, source class, geography, specialty, topic, and time window,
- AI-generated summaries and translations,
- source traceability and credibility labeling,
- event deduplication and clustering support.

This schema is intentionally aligned with the MVP defined in the Product Requirements Document.

## 2. Scope and Design Principles

### 2.1 MVP Layer Alignment
The schema must support the following five MVP content layers:
1. Public Health / Surveillance
2. Guidelines / Official Updates
3. Scientific Literature
4. Preprints
5. Pharmacovigilance / Drug Safety

### 2.2 Core Design Principles
- Separate **raw ingested records** from **canonical display events**.
- Preserve **full source traceability**.
- Use **normalized taxonomies** instead of storing tag IDs in arrays.
- Support **nullable geolocation** because not every event has precise coordinates.
- Separate **source publication time**, **event occurrence time**, and **system ingestion time**.
- Support **machine-translated summaries** without replacing original source text.
- Support **canonical event grouping** for deduplication.
- Optimize for **PostgreSQL + PostGIS** and API-driven filtering.

## 3. High-Level Entity Model

The MVP schema is organized around the following entity groups:

### 3.1 Source and Ingestion
- `source_providers`
- `source_feeds`
- `ingestion_runs`
- `raw_documents`

### 3.2 Canonical Event Layer
- `events`
- `event_source_links`
- `event_locations`
- `event_translations`

### 3.3 Taxonomy and Filtering
- `layers`
- `source_classes`
- `trust_tiers`
- `evidence_statuses`
- `specialties`
- `topics`
- `organizations`
- `jurisdictions`

### 3.4 Join Tables
- `event_topics`
- `event_specialties`
- `event_organizations`

### 3.5 Operations and Audit
- `ai_processing_jobs`
- `event_change_log`

## 4. Main Tables

---

## 4.1 `source_providers`

Represents a source organization or data provider.

Examples:
- World Health Organization
- ECDC
- PubMed / NCBI
- Europe PMC
- medRxiv
- FDA / openFDA

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Provider identifier |
| name | VARCHAR(255) | NOT NULL | Display name |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | Stable identifier |
| source_class_id | SMALLINT | FK, NOT NULL | Official authority, scientific database, preprint server, media, etc. |
| trust_tier_id | SMALLINT | FK, NOT NULL | Default credibility tier |
| homepage_url | TEXT | NULL | Provider homepage |
| default_language_code | VARCHAR(10) | NULL | Main language if known |
| country_code | CHAR(2) | NULL | ISO country code if relevant |
| is_active | BOOLEAN | NOT NULL DEFAULT TRUE | Provider status |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Update timestamp |

Indexes:
- unique index on `slug`
- index on `source_class_id`
- index on `trust_tier_id`

---

## 4.2 `source_feeds`

Represents a specific API endpoint, RSS feed, or structured source channel.

Examples:
- WHO RSS outbreak feed
- PubMed query endpoint
- ECDC news RSS
- openFDA recalls endpoint

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Feed identifier |
| provider_id | UUID | FK, NOT NULL | Parent provider |
| name | VARCHAR(255) | NOT NULL | Feed name |
| feed_type | VARCHAR(50) | NOT NULL | rss, api, scraper, manual, webhook |
| endpoint_url | TEXT | NOT NULL | Feed endpoint |
| default_layer_id | SMALLINT | FK, NOT NULL | Default HealthMonitor layer |
| polling_interval_minutes | INTEGER | NOT NULL | Intended refresh interval |
| is_active | BOOLEAN | NOT NULL DEFAULT TRUE | Feed status |
| last_success_at | TIMESTAMPTZ | NULL | Last successful ingestion |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Update timestamp |

Indexes:
- index on `provider_id`
- index on `default_layer_id`
- index on `is_active`

---

## 4.3 `ingestion_runs`

Tracks ingestion job executions for each feed.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Run identifier |
| source_feed_id | UUID | FK, NOT NULL | Feed being processed |
| status | VARCHAR(30) | NOT NULL | queued, running, success, partial_success, failed |
| started_at | TIMESTAMPTZ | NOT NULL | Run start |
| finished_at | TIMESTAMPTZ | NULL | Run end |
| records_fetched | INTEGER | NOT NULL DEFAULT 0 | Raw records retrieved |
| records_inserted | INTEGER | NOT NULL DEFAULT 0 | Raw records stored |
| records_promoted | INTEGER | NOT NULL DEFAULT 0 | Canonical events created/updated |
| error_message | TEXT | NULL | Failure message if any |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- index on `source_feed_id`
- index on `status`
- index on `started_at`

---

## 4.4 `raw_documents`

Stores the original ingested records before normalization.

This table is critical for traceability, reprocessing, and deduplication.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Raw document identifier |
| ingestion_run_id | UUID | FK, NOT NULL | Ingestion run |
| source_feed_id | UUID | FK, NOT NULL | Origin feed |
| provider_id | UUID | FK, NOT NULL | Origin provider |
| external_document_id | VARCHAR(255) | NULL | Source-native ID if available |
| original_title | TEXT | NULL | Original title in original language |
| original_url | TEXT | NOT NULL | Original source URL |
| original_language_code | VARCHAR(10) | NULL | Original language |
| source_published_at | TIMESTAMPTZ | NULL | Publication timestamp from source |
| fetched_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | System fetch time |
| raw_payload_json | JSONB | NOT NULL | Full source payload |
| content_hash | VARCHAR(128) | NOT NULL | Hash of core raw content |
| parsing_status | VARCHAR(30) | NOT NULL DEFAULT 'parsed' | parsed, failed, skipped |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Constraints and indexes:
- unique index on `(source_feed_id, external_document_id)` where `external_document_id IS NOT NULL`
- unique index on `(source_feed_id, original_url)`
- index on `provider_id`
- index on `source_published_at`
- index on `content_hash`
- GIN index on `raw_payload_json`

---

## 4.5 `events`

Represents canonical events displayed in the application.

An event may be derived from one or multiple raw documents.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Canonical event identifier |
| canonical_group_id | UUID | NULL | Shared identifier for grouped duplicates/variants |
| primary_raw_document_id | UUID | FK, NULL | Main raw record used for display |
| layer_id | SMALLINT | FK, NOT NULL | Public Health, Guidelines, Literature, Preprints, Pharmacovigilance |
| title | TEXT | NOT NULL | Canonical display title |
| relevance_label | VARCHAR(255) | NULL | Short explanatory label |
| summary_en | TEXT | NULL | English AI summary |
| original_language_code | VARCHAR(10) | NULL | Original language of primary source |
| source_published_at | TIMESTAMPTZ | NULL | Publication timestamp from source |
| event_occurred_at | TIMESTAMPTZ | NULL | Real-world occurrence time if distinct |
| ingested_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | First creation time in system |
| updated_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Last canonical update |
| primary_provider_id | UUID | FK, NOT NULL | Main provider shown in UI |
| evidence_status_id | SMALLINT | FK, NOT NULL | guideline, peer_reviewed, preprint, regulatory_notice, etc. |
| trust_tier_id | SMALLINT | FK, NOT NULL | high, moderate, exploratory |
| geographic_scope | VARCHAR(30) | NOT NULL | local, national, regional, global |
| country_code | CHAR(2) | NULL | Main country if available |
| region_code | VARCHAR(20) | NULL | Internal region preset code |
| location_name | VARCHAR(255) | NULL | Human-readable location |
| location_point | GEOGRAPHY(Point, 4326) | NULL | Map coordinate when available |
| geo_precision | VARCHAR(30) | NULL | point, city, country, region, global, unknown |
| is_active | BOOLEAN | NOT NULL DEFAULT TRUE | Active status |
| visibility_status | VARCHAR(30) | NOT NULL DEFAULT 'visible' | visible, hidden, archived |
| review_status | VARCHAR(30) | NOT NULL DEFAULT 'auto' | auto, reviewed, flagged |
| severity_level | VARCHAR(20) | NULL | low, medium, high, critical, nullable |
| dedupe_key | VARCHAR(255) | NULL | Hash/key used in duplicate detection |
| duplicate_of_event_id | UUID | FK, NULL | Pointer if this record is marked duplicate |
| metadata_json | JSONB | NULL | Layer-specific structured metadata |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- index on `layer_id`
- index on `source_published_at DESC`
- index on `event_occurred_at DESC`
- index on `primary_provider_id`
- index on `trust_tier_id`
- index on `evidence_status_id`
- index on `country_code`
- index on `region_code`
- index on `visibility_status`
- index on `is_active`
- index on `duplicate_of_event_id`
- index on `canonical_group_id`
- GIST index on `location_point`
- GIN index on `metadata_json`
- GIN full-text index on `title` and `summary_en`
- trigram index on `title`

Notes:
- `freshness` must be computed from timestamps at query or presentation time, not stored as a text field.
- `location_point` is nullable by design.
- `metadata_json` holds layer-specific attributes such as regulator name, study design, outbreak counts, or guideline issuer details.

---

## 4.6 `event_source_links`

Links canonical events to one or more source records.

This table preserves traceability and supports “open original source” behavior.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Link identifier |
| event_id | UUID | FK, NOT NULL | Canonical event |
| raw_document_id | UUID | FK, NOT NULL | Source raw document |
| provider_id | UUID | FK, NOT NULL | Source provider |
| relationship_type | VARCHAR(30) | NOT NULL | primary, corroborating, duplicate_source, update_source |
| is_display_source | BOOLEAN | NOT NULL DEFAULT FALSE | Whether shown by default in UI |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- unique index on `(event_id, raw_document_id)`
- index on `provider_id`
- index on `relationship_type`

---

## 4.7 `event_translations`

Stores translated summaries and translated UI-facing event text.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Translation identifier |
| event_id | UUID | FK, NOT NULL | Parent event |
| language_code | VARCHAR(10) | NOT NULL | fr, etc. |
| translated_summary | TEXT | NOT NULL | Machine-translated summary |
| translated_relevance_label | VARCHAR(255) | NULL | Optional translated label |
| translation_provider | VARCHAR(50) | NOT NULL | deepl, manual, etc. |
| is_machine_translated | BOOLEAN | NOT NULL DEFAULT TRUE | Machine translation flag |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Update timestamp |

Indexes:
- unique index on `(event_id, language_code)`
- index on `language_code`

---

## 4.8 `event_locations`

Optional secondary locations associated with an event.

Use this table when an event is relevant to multiple countries or places.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Location identifier |
| event_id | UUID | FK, NOT NULL | Parent event |
| location_name | VARCHAR(255) | NOT NULL | Display name |
| country_code | CHAR(2) | NULL | ISO country code |
| region_code | VARCHAR(20) | NULL | Internal region preset code |
| location_point | GEOGRAPHY(Point, 4326) | NULL | Coordinate if available |
| geo_precision | VARCHAR(30) | NOT NULL DEFAULT 'unknown' | point, city, country, region, global |
| is_primary | BOOLEAN | NOT NULL DEFAULT FALSE | Primary map location |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- index on `event_id`
- index on `country_code`
- GIST index on `location_point`

## 5. Taxonomy and Reference Tables

---

## 5.1 `layers`

Defines the five MVP application layers.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | SMALLSERIAL | PK | Layer ID |
| code | VARCHAR(30) | UNIQUE, NOT NULL | Layer code |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Layer name |
| description | TEXT | NULL | Layer description |
| is_mvp | BOOLEAN | NOT NULL DEFAULT TRUE | MVP membership |
| sort_order | SMALLINT | NOT NULL | UI order |

MVP seed values:
- `PUB_HEALTH`
- `GUIDELINES`
- `LITERATURE`
- `PREPRINTS`
- `PHARMACOVIGILANCE`

---

## 5.2 `source_classes`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | SMALLSERIAL | PK | Source class ID |
| code | VARCHAR(30) | UNIQUE, NOT NULL | Code |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Display name |

Suggested seed values:
- `OFFICIAL_AUTHORITY`
- `SCIENTIFIC_DATABASE`
- `PREPRINT_SERVER`
- `REGULATORY_DATABASE`
- `MEDIA`

---

## 5.3 `trust_tiers`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | SMALLSERIAL | PK | Trust tier ID |
| code | VARCHAR(30) | UNIQUE, NOT NULL | Code |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Display name |
| sort_order | SMALLINT | NOT NULL | Ordering |

Suggested seed values:
- `HIGH`
- `MODERATE`
- `EXPLORATORY`

---

## 5.4 `evidence_statuses`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | SMALLSERIAL | PK | Evidence status ID |
| code | VARCHAR(40) | UNIQUE, NOT NULL | Code |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Display name |

Suggested seed values:
- `SURVEILLANCE_REPORT`
- `GUIDELINE`
- `PEER_REVIEWED_ARTICLE`
- `PREPRINT`
- `REGULATORY_NOTICE`
- `MEDIA_REPORT`

---

## 5.5 `specialties`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Specialty ID |
| code | VARCHAR(50) | UNIQUE, NOT NULL | Code |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Display name |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Examples:
- infectious_disease
- pharmacy
- laboratory_medicine
- oncology
- public_health

---

## 5.6 `topics`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Topic ID |
| code | VARCHAR(100) | UNIQUE, NOT NULL | Code |
| name | VARCHAR(255) | NOT NULL | Display name |
| topic_type | VARCHAR(50) | NOT NULL | disease, pathogen, drug, vaccine, policy, syndrome |
| parent_topic_id | UUID | FK, NULL | Optional hierarchy |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

---

## 5.7 `organizations`

Used for guideline issuers, regulatory bodies, journals, or institutional actors when they need explicit filtering.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Organization ID |
| name | VARCHAR(255) | NOT NULL | Organization name |
| slug | VARCHAR(120) | UNIQUE, NOT NULL | Stable identifier |
| org_type | VARCHAR(50) | NOT NULL | regulator, journal, society, agency, university |
| country_code | CHAR(2) | NULL | ISO country code |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

---

## 5.8 `jurisdictions`

Represents country or supra-country applicability zones.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Jurisdiction ID |
| code | VARCHAR(30) | UNIQUE, NOT NULL | Code |
| name | VARCHAR(100) | NOT NULL | Name |
| jurisdiction_type | VARCHAR(30) | NOT NULL | country, region, union, global |
| country_code | CHAR(2) | NULL | ISO code if country |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

## 6. Join Tables

---

## 6.1 `event_topics`

| Column | Type | Constraints | Description |
|---|---|---|---|
| event_id | UUID | FK, PK(partial) | Event |
| topic_id | UUID | FK, PK(partial) | Topic |
| is_primary | BOOLEAN | NOT NULL DEFAULT FALSE | Primary topic flag |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- primary key on `(event_id, topic_id)`
- index on `topic_id`

---

## 6.2 `event_specialties`

| Column | Type | Constraints | Description |
|---|---|---|---|
| event_id | UUID | FK, PK(partial) | Event |
| specialty_id | UUID | FK, PK(partial) | Specialty |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- primary key on `(event_id, specialty_id)`
- index on `specialty_id`

---

## 6.3 `event_organizations`

| Column | Type | Constraints | Description |
|---|---|---|---|
| event_id | UUID | FK, PK(partial) | Event |
| organization_id | UUID | FK, PK(partial) | Organization |
| relationship_type | VARCHAR(40) | NOT NULL | issuer, regulator, sponsor, publisher |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- primary key on `(event_id, organization_id, relationship_type)`
- index on `organization_id`

## 7. AI and Audit Tables

---

## 7.1 `ai_processing_jobs`

Tracks summarization and translation processing.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Job identifier |
| event_id | UUID | FK, NOT NULL | Parent event |
| job_type | VARCHAR(30) | NOT NULL | summary, translation |
| provider_name | VARCHAR(50) | NOT NULL | openai, deepl, etc. |
| status | VARCHAR(30) | NOT NULL | queued, running, success, failed |
| input_hash | VARCHAR(128) | NOT NULL | Input signature |
| output_hash | VARCHAR(128) | NULL | Output signature |
| started_at | TIMESTAMPTZ | NULL | Start timestamp |
| finished_at | TIMESTAMPTZ | NULL | End timestamp |
| error_message | TEXT | NULL | Failure text |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- index on `event_id`
- index on `job_type`
- index on `status`

---

## 7.2 `event_change_log`

Stores event-level audit history for debugging and reprocessing.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Log identifier |
| event_id | UUID | FK, NOT NULL | Event |
| change_type | VARCHAR(40) | NOT NULL | created, updated, merged, hidden, translated |
| changed_by | VARCHAR(50) | NOT NULL | system, worker, admin |
| change_payload_json | JSONB | NULL | Structured change details |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Creation timestamp |

Indexes:
- index on `event_id`
- index on `change_type`
- index on `created_at`

## 8. Relationship Summary

### One-to-many
- one `source_provider` → many `source_feeds`
- one `source_feed` → many `ingestion_runs`
- one `ingestion_run` → many `raw_documents`
- one `event` → many `event_source_links`
- one `event` → many `event_translations`
- one `event` → many `event_locations`

### Many-to-many
- many `events` ↔ many `topics`
- many `events` ↔ many `specialties`
- many `events` ↔ many `organizations`

### Canonical mapping
- many `raw_documents` may map to one `event`
- many duplicate or corroborating events may share one `canonical_group_id`

## 9. Query Patterns the Schema Must Support

The schema must efficiently support the following MVP query patterns:

1. Retrieve visible events by:
   - map viewport / bounding box,
   - layer,
   - time window,
   - source class,
   - trust tier,
   - topic,
   - specialty,
   - country or region.

2. Retrieve compact event card data with:
   - canonical event fields,
   - primary source,
   - source class,
   - trust tier,
   - translated summary if available.

3. Retrieve region-level counts for:
   - total events,
   - events by layer,
   - top topics,
   - top source classes.

4. Search events by:
   - keyword,
   - topic,
   - provider,
   - organization,
   - date range.

5. Reprocess events when:
   - a summarization prompt changes,
   - translation is retried,
   - source taxonomy mapping is updated.

## 10. Indexing Strategy

Recommended MVP indexes:
- GIST on `events.location_point`
- GIST on `event_locations.location_point`
- B-tree on event time fields
- B-tree on `layer_id`, `primary_provider_id`, `country_code`, `trust_tier_id`
- GIN full-text index on event `title` + `summary_en`
- trigram index on event `title`
- GIN on `raw_documents.raw_payload_json`
- B-tree on join-table foreign keys

## 11. Data Retention and Archiving

For MVP:
- keep `raw_documents` for traceability and reprocessing,
- keep inactive or hidden `events` instead of hard-deleting them,
- archive old ingestion runs but retain operational metrics,
- preserve source links even when an event is merged into a canonical group.

## 12. Deferred / Phase 2 Schema Extensions

The following are intentionally out of MVP schema scope:
- user accounts and saved views,
- bookmarks and alerts,
- comment or annotation system,
- live video ingestion metadata,
- advanced trend snapshots,
- ClinicalTrials-specific structured tables,
- multilingual source title translations beyond MVP requirements,
- manual editorial workflow tables.

These may be introduced later without breaking the core data model.
