import uuid

from geoalchemy2 import Geography
from sqlalchemy import Boolean, DateTime, ForeignKey, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    canonical_group_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    primary_raw_document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("raw_documents.id", ondelete="SET NULL"), nullable=True
    )
    layer_id: Mapped[int] = mapped_column(
        ForeignKey("layers.id", ondelete="RESTRICT"), nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    relevance_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_language_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    source_published_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    event_occurred_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ingested_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    primary_provider_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("source_providers.id", ondelete="RESTRICT"), nullable=False
    )
    evidence_status_id: Mapped[int] = mapped_column(
        ForeignKey("evidence_statuses.id", ondelete="RESTRICT"), nullable=False
    )
    trust_tier_id: Mapped[int] = mapped_column(
        ForeignKey("trust_tiers.id", ondelete="RESTRICT"), nullable=False
    )
    geographic_scope: Mapped[str] = mapped_column(String(30), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    region_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    location_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location_point: Mapped[Geography | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=True
    )
    geo_precision: Mapped[str | None] = mapped_column(String(30), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    visibility_status: Mapped[str] = mapped_column(String(30), nullable=False, default="visible")
    review_status: Mapped[str] = mapped_column(String(30), nullable=False, default="auto")
    severity_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    dedupe_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    duplicate_of_event_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("events.id", ondelete="SET NULL"), nullable=True
    )
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class EventSourceLink(Base):
    __tablename__ = "event_source_links"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    raw_document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("raw_documents.id", ondelete="CASCADE"), nullable=False
    )
    provider_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("source_providers.id", ondelete="CASCADE"), nullable=False
    )
    relationship_type: Mapped[str] = mapped_column(String(30), nullable=False)
    is_display_source: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class EventTranslation(Base):
    __tablename__ = "event_translations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    translated_summary: Mapped[str] = mapped_column(Text, nullable=False)
    translated_relevance_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    translation_provider: Mapped[str] = mapped_column(String(50), nullable=False)
    is_machine_translated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class EventLocation(Base):
    __tablename__ = "event_locations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    region_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    location_point: Mapped[Geography | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=True
    )
    geo_precision: Mapped[str] = mapped_column(String(30), nullable=False, default="unknown")
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
