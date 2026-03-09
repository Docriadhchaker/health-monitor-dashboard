import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_feed_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("source_feeds.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    started_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    records_fetched: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    records_inserted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    records_promoted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RawDocument(Base):
    __tablename__ = "raw_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ingestion_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ingestion_runs.id", ondelete="CASCADE"), nullable=False
    )
    source_feed_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("source_feeds.id", ondelete="CASCADE"), nullable=False
    )
    provider_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("source_providers.id", ondelete="CASCADE"), nullable=False
    )
    external_document_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    original_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    original_language_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    source_published_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    fetched_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    raw_payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    parsing_status: Mapped[str] = mapped_column(String(30), nullable=False, default="parsed")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
