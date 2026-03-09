"""initial_schema

Revision ID: 001
Revises:
Create Date: 2025-03-09

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geography

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    op.create_table(
        "layers",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_mvp", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("sort_order", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_layers_code", "layers", ["code"], unique=True)
    op.create_index("ix_layers_name", "layers", ["name"], unique=True)

    op.create_table(
        "source_classes",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_source_classes_code", "source_classes", ["code"], unique=True)
    op.create_index("ix_source_classes_name", "source_classes", ["name"], unique=True)

    op.create_table(
        "trust_tiers",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("sort_order", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_trust_tiers_code", "trust_tiers", ["code"], unique=True)
    op.create_index("ix_trust_tiers_name", "trust_tiers", ["name"], unique=True)

    op.create_table(
        "evidence_statuses",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(40), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_statuses_code", "evidence_statuses", ["code"], unique=True)
    op.create_index("ix_evidence_statuses_name", "evidence_statuses", ["name"], unique=True)

    op.create_table(
        "source_providers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("source_class_id", sa.SmallInteger(), nullable=False),
        sa.Column("trust_tier_id", sa.SmallInteger(), nullable=False),
        sa.Column("homepage_url", sa.Text(), nullable=True),
        sa.Column("default_language_code", sa.String(10), nullable=True),
        sa.Column("country_code", sa.String(2), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["source_class_id"], ["source_classes.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["trust_tier_id"], ["trust_tiers.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_source_providers_slug", "source_providers", ["slug"], unique=True)
    op.create_index("ix_source_providers_source_class_id", "source_providers", ["source_class_id"])
    op.create_index("ix_source_providers_trust_tier_id", "source_providers", ["trust_tier_id"])

    op.create_table(
        "source_feeds",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("provider_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("feed_type", sa.String(50), nullable=False),
        sa.Column("endpoint_url", sa.Text(), nullable=False),
        sa.Column("default_layer_id", sa.SmallInteger(), nullable=False),
        sa.Column("polling_interval_minutes", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_success_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["default_layer_id"], ["layers.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["provider_id"], ["source_providers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_source_feeds_provider_id", "source_feeds", ["provider_id"])
    op.create_index("ix_source_feeds_default_layer_id", "source_feeds", ["default_layer_id"])
    op.create_index("ix_source_feeds_is_active", "source_feeds", ["is_active"])

    op.create_table(
        "ingestion_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("source_feed_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("records_fetched", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_inserted", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_promoted", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["source_feed_id"], ["source_feeds.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ingestion_runs_source_feed_id", "ingestion_runs", ["source_feed_id"])
    op.create_index("ix_ingestion_runs_status", "ingestion_runs", ["status"])
    op.create_index("ix_ingestion_runs_started_at", "ingestion_runs", ["started_at"])

    op.create_table(
        "raw_documents",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("ingestion_run_id", sa.Uuid(), nullable=False),
        sa.Column("source_feed_id", sa.Uuid(), nullable=False),
        sa.Column("provider_id", sa.Uuid(), nullable=False),
        sa.Column("external_document_id", sa.String(255), nullable=True),
        sa.Column("original_title", sa.Text(), nullable=True),
        sa.Column("original_url", sa.Text(), nullable=False),
        sa.Column("original_language_code", sa.String(10), nullable=True),
        sa.Column("source_published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw_payload_json", sa.dialects.postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("content_hash", sa.String(128), nullable=False),
        sa.Column("parsing_status", sa.String(30), nullable=False, server_default="'parsed'"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["ingestion_run_id"], ["ingestion_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["provider_id"], ["source_providers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_feed_id"], ["source_feeds.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_raw_documents_provider_id", "raw_documents", ["provider_id"])
    op.create_index("ix_raw_documents_source_published_at", "raw_documents", ["source_published_at"])
    op.create_index("ix_raw_documents_content_hash", "raw_documents", ["content_hash"])
    op.create_index("ix_raw_documents_raw_payload_json", "raw_documents", ["raw_payload_json"], postgresql_using="gin")
    op.create_index(
        "uq_raw_documents_feed_external_id",
        "raw_documents",
        ["source_feed_id", "external_document_id"],
        unique=True,
        postgresql_where=sa.text("external_document_id IS NOT NULL"),
    )
    op.create_index("uq_raw_documents_feed_url", "raw_documents", ["source_feed_id", "original_url"], unique=True)

    op.create_table(
        "events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("canonical_group_id", sa.Uuid(), nullable=True),
        sa.Column("primary_raw_document_id", sa.Uuid(), nullable=True),
        sa.Column("layer_id", sa.SmallInteger(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("relevance_label", sa.String(255), nullable=True),
        sa.Column("summary_en", sa.Text(), nullable=True),
        sa.Column("original_language_code", sa.String(10), nullable=True),
        sa.Column("source_published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("event_occurred_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ingested_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("primary_provider_id", sa.Uuid(), nullable=False),
        sa.Column("evidence_status_id", sa.SmallInteger(), nullable=False),
        sa.Column("trust_tier_id", sa.SmallInteger(), nullable=False),
        sa.Column("geographic_scope", sa.String(30), nullable=False),
        sa.Column("country_code", sa.String(2), nullable=True),
        sa.Column("region_code", sa.String(20), nullable=True),
        sa.Column("location_name", sa.String(255), nullable=True),
        sa.Column("location_point", Geography(geometry_type="POINT", srid=4326), nullable=True),
        sa.Column("geo_precision", sa.String(30), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("visibility_status", sa.String(30), nullable=False, server_default="'visible'"),
        sa.Column("review_status", sa.String(30), nullable=False, server_default="'auto'"),
        sa.Column("severity_level", sa.String(20), nullable=True),
        sa.Column("dedupe_key", sa.String(255), nullable=True),
        sa.Column("duplicate_of_event_id", sa.Uuid(), nullable=True),
        sa.Column("metadata_json", sa.dialects.postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["duplicate_of_event_id"], ["events.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["evidence_status_id"], ["evidence_statuses.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["layer_id"], ["layers.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["primary_provider_id"], ["source_providers.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["primary_raw_document_id"], ["raw_documents.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["trust_tier_id"], ["trust_tiers.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_events_layer_id", "events", ["layer_id"])
    op.create_index("ix_events_source_published_at", "events", [sa.text("source_published_at DESC")])
    op.create_index("ix_events_event_occurred_at", "events", [sa.text("event_occurred_at DESC")])
    op.create_index("ix_events_primary_provider_id", "events", ["primary_provider_id"])
    op.create_index("ix_events_trust_tier_id", "events", ["trust_tier_id"])
    op.create_index("ix_events_evidence_status_id", "events", ["evidence_status_id"])
    op.create_index("ix_events_country_code", "events", ["country_code"])
    op.create_index("ix_events_region_code", "events", ["region_code"])
    op.create_index("ix_events_visibility_status", "events", ["visibility_status"])
    op.create_index("ix_events_is_active", "events", ["is_active"])
    op.create_index("ix_events_duplicate_of_event_id", "events", ["duplicate_of_event_id"])
    op.create_index("ix_events_canonical_group_id", "events", ["canonical_group_id"])
    op.create_index("ix_events_location_point", "events", ["location_point"], postgresql_using="gist")
    op.create_index("ix_events_metadata_json", "events", ["metadata_json"], postgresql_using="gin")
    op.execute(
        "CREATE INDEX ix_events_title_summary_fts ON events "
        "USING gin(to_tsvector('english', coalesce(title, '') || ' ' || coalesce(summary_en, '')))"
    )
    op.execute("CREATE INDEX ix_events_title_trgm ON events USING gin (title gin_trgm_ops)")

    op.create_table(
        "event_source_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("raw_document_id", sa.Uuid(), nullable=False),
        sa.Column("provider_id", sa.Uuid(), nullable=False),
        sa.Column("relationship_type", sa.String(30), nullable=False),
        sa.Column("is_display_source", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["provider_id"], ["source_providers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["raw_document_id"], ["raw_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_event_source_links_event_raw", "event_source_links", ["event_id", "raw_document_id"], unique=True)
    op.create_index("ix_event_source_links_provider_id", "event_source_links", ["provider_id"])
    op.create_index("ix_event_source_links_relationship_type", "event_source_links", ["relationship_type"])

    op.create_table(
        "event_translations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(10), nullable=False),
        sa.Column("translated_summary", sa.Text(), nullable=False),
        sa.Column("translated_relevance_label", sa.String(255), nullable=True),
        sa.Column("translation_provider", sa.String(50), nullable=False),
        sa.Column("is_machine_translated", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_event_translations_event_lang", "event_translations", ["event_id", "language_code"], unique=True)
    op.create_index("ix_event_translations_language_code", "event_translations", ["language_code"])

    op.create_table(
        "event_locations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("location_name", sa.String(255), nullable=False),
        sa.Column("country_code", sa.String(2), nullable=True),
        sa.Column("region_code", sa.String(20), nullable=True),
        sa.Column("location_point", Geography(geometry_type="POINT", srid=4326), nullable=True),
        sa.Column("geo_precision", sa.String(30), nullable=False, server_default="'unknown'"),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_event_locations_event_id", "event_locations", ["event_id"])
    op.create_index("ix_event_locations_country_code", "event_locations", ["country_code"])
    op.create_index("ix_event_locations_location_point", "event_locations", ["location_point"], postgresql_using="gist")

    op.create_table(
        "specialties",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_specialties_code", "specialties", ["code"], unique=True)
    op.create_index("ix_specialties_name", "specialties", ["name"], unique=True)

    op.create_table(
        "topics",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("topic_type", sa.String(50), nullable=False),
        sa.Column("parent_topic_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["parent_topic_id"], ["topics.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_topics_code", "topics", ["code"], unique=True)

    op.create_table(
        "organizations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(120), nullable=False),
        sa.Column("org_type", sa.String(50), nullable=False),
        sa.Column("country_code", sa.String(2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_organizations_slug", "organizations", ["slug"], unique=True)

    op.create_table(
        "jurisdictions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("jurisdiction_type", sa.String(30), nullable=False),
        sa.Column("country_code", sa.String(2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_jurisdictions_code", "jurisdictions", ["code"], unique=True)

    op.create_table(
        "event_topics",
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("topic_id", sa.Uuid(), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("event_id", "topic_id"),
    )
    op.create_index("ix_event_topics_topic_id", "event_topics", ["topic_id"])

    op.create_table(
        "event_specialties",
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("specialty_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["specialty_id"], ["specialties.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("event_id", "specialty_id"),
    )
    op.create_index("ix_event_specialties_specialty_id", "event_specialties", ["specialty_id"])

    op.create_table(
        "event_organizations",
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("relationship_type", sa.String(40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("event_id", "organization_id", "relationship_type"),
    )
    op.create_index("ix_event_organizations_organization_id", "event_organizations", ["organization_id"])

    op.create_table(
        "ai_processing_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("job_type", sa.String(30), nullable=False),
        sa.Column("provider_name", sa.String(50), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("input_hash", sa.String(128), nullable=False),
        sa.Column("output_hash", sa.String(128), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_processing_jobs_event_id", "ai_processing_jobs", ["event_id"])
    op.create_index("ix_ai_processing_jobs_job_type", "ai_processing_jobs", ["job_type"])
    op.create_index("ix_ai_processing_jobs_status", "ai_processing_jobs", ["status"])

    op.create_table(
        "event_change_log",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("change_type", sa.String(40), nullable=False),
        sa.Column("changed_by", sa.String(50), nullable=False),
        sa.Column("change_payload_json", sa.dialects.postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_event_change_log_event_id", "event_change_log", ["event_id"])
    op.create_index("ix_event_change_log_change_type", "event_change_log", ["change_type"])
    op.create_index("ix_event_change_log_created_at", "event_change_log", ["created_at"])


def downgrade() -> None:
    op.drop_table("event_change_log")
    op.drop_table("ai_processing_jobs")
    op.drop_table("event_organizations")
    op.drop_table("event_specialties")
    op.drop_table("event_topics")
    op.drop_table("jurisdictions")
    op.drop_table("organizations")
    op.drop_table("topics")
    op.drop_table("specialties")
    op.drop_table("event_locations")
    op.drop_table("event_translations")
    op.drop_table("event_source_links")
    op.drop_table("events")
    op.drop_table("raw_documents")
    op.drop_table("ingestion_runs")
    op.drop_table("source_feeds")
    op.drop_table("source_providers")
    op.drop_table("evidence_statuses")
    op.drop_table("trust_tiers")
    op.drop_table("source_classes")
    op.drop_table("layers")
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
    op.execute("DROP EXTENSION IF EXISTS postgis")
