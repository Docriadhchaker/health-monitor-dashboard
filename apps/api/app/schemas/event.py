from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EventListQuery(BaseModel):
    """Query params for GET /api/v1/events."""

    layer_ids: list[int] | None = Field(None, description="Filter by layer id(s)")
    region_code: str | None = Field(None, description="Region preset: WORLD, EUROPE, etc.")
    country_code: str | None = Field(None, description="ISO country code")
    time_window: str | None = Field(None, description="24h, 7d, 30d")
    source_class_id: int | None = Field(None, description="Filter by source class")
    trust_tier_id: int | None = Field(None, description="Filter by trust tier")
    min_lon: float | None = Field(None, description="Bbox min longitude")
    min_lat: float | None = Field(None, description="Bbox min latitude")
    max_lon: float | None = Field(None, description="Bbox max longitude")
    max_lat: float | None = Field(None, description="Bbox max latitude")
    limit: int = Field(500, ge=1, le=2000)
    offset: int = Field(0, ge=0)


class EventListItem(BaseModel):
    """Compact event for map markers and list."""

    id: UUID
    title: str
    layer_id: int
    layer_code: str
    layer_name: str
    source_class_id: int
    source_class_name: str
    trust_tier_id: int
    trust_tier_name: str
    evidence_status_id: int
    evidence_status_name: str
    source_name: str
    source_url: str | None
    source_published_at: datetime | None
    country_code: str | None
    region_code: str | None
    location_name: str | None
    lat: float | None
    lon: float | None
    summary_en: str | None
    geographic_scope: str
    geo_precision: str | None = None

    model_config = {"from_attributes": True}


class EventTranslationOut(BaseModel):
    language_code: str
    translated_summary: str
    is_machine_translated: bool


class EventDetail(BaseModel):
    """Full event for compact card."""

    id: UUID
    title: str
    layer_id: int
    layer_code: str
    layer_name: str
    source_class_id: int
    source_class_name: str
    trust_tier_id: int
    trust_tier_name: str
    evidence_status_id: int
    evidence_status_name: str
    source_name: str
    source_url: str | None
    source_published_at: datetime | None
    ingested_at: datetime | None = None
    event_occurred_at: datetime | None
    country_code: str | None
    region_code: str | None
    location_name: str | None
    geographic_scope: str
    geo_precision: str | None = None
    summary_en: str | None
    relevance_label: str | None
    specialty_names: list[str] = Field(default_factory=list)
    topic_names: list[str] = Field(default_factory=list)
    translations: list[EventTranslationOut] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    items: list[EventListItem]
    total: int
