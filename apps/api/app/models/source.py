import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class SourceProvider(Base):
    __tablename__ = "source_providers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    source_class_id: Mapped[int] = mapped_column(
        ForeignKey("source_classes.id", ondelete="RESTRICT"), nullable=False
    )
    trust_tier_id: Mapped[int] = mapped_column(
        ForeignKey("trust_tiers.id", ondelete="RESTRICT"), nullable=False
    )
    homepage_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    default_language_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SourceFeed(Base):
    __tablename__ = "source_feeds"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("source_providers.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    feed_type: Mapped[str] = mapped_column(String(50), nullable=False)
    endpoint_url: Mapped[str] = mapped_column(Text, nullable=False)
    default_layer_id: Mapped[int] = mapped_column(
        ForeignKey("layers.id", ondelete="RESTRICT"), nullable=False
    )
    polling_interval_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_success_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
