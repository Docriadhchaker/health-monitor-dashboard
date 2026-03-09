from datetime import datetime, timedelta, timezone
from uuid import UUID

from geoalchemy2 import functions as geo_funcs
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import (
    Event,
    EventSourceLink,
    EventSpecialty,
    EventTranslation,
    EventTopic,
    EvidenceStatus,
    Layer,
    RawDocument,
    SourceClass,
    SourceProvider,
    Specialty,
    Topic,
    TrustTier,
)


def _time_cutoff(time_window: str | None) -> datetime | None:
    if not time_window:
        return None
    now = datetime.now(timezone.utc)
    if time_window == "24h":
        return now - timedelta(hours=24)
    if time_window == "7d":
        return now - timedelta(days=7)
    if time_window == "30d":
        return now - timedelta(days=30)
    return None


def list_events(
    db: Session,
    *,
    layer_ids: list[int] | None = None,
    region_code: str | None = None,
    country_code: str | None = None,
    time_window: str | None = None,
    source_class_id: int | None = None,
    trust_tier_id: int | None = None,
    min_lon: float | None = None,
    min_lat: float | None = None,
    max_lon: float | None = None,
    max_lat: float | None = None,
    limit: int = 500,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """Return (list of event dicts for EventListItem, total count)."""
    q = (
        db.query(
            Event,
            Layer.code.label("layer_code"),
            Layer.name.label("layer_name"),
            SourceClass.id.label("source_class_id"),
            SourceClass.name.label("source_class_name"),
            TrustTier.name.label("trust_tier_name"),
            EvidenceStatus.name.label("evidence_status_name"),
            SourceProvider.name.label("source_name"),
        )
        .join(Layer, Event.layer_id == Layer.id)
        .join(SourceProvider, Event.primary_provider_id == SourceProvider.id)
        .join(SourceClass, SourceProvider.source_class_id == SourceClass.id)
        .join(TrustTier, Event.trust_tier_id == TrustTier.id)
        .join(EvidenceStatus, Event.evidence_status_id == EvidenceStatus.id)
        .filter(Event.visibility_status == "visible", Event.is_active == True)
    )

    if layer_ids:
        q = q.filter(Event.layer_id.in_(layer_ids))
    if region_code and region_code.upper() != "WORLD":
        q = q.filter(Event.region_code == region_code.upper())
    if country_code:
        q = q.filter(Event.country_code == country_code.upper())
    if time_window:
        cutoff = _time_cutoff(time_window)
        if cutoff:
            q = q.filter(or_(Event.source_published_at >= cutoff, Event.ingested_at >= cutoff))
    if source_class_id:
        q = q.filter(SourceProvider.source_class_id == source_class_id)
    if trust_tier_id:
        q = q.filter(Event.trust_tier_id == trust_tier_id)
    if min_lon is not None and max_lon is not None and min_lat is not None and max_lat is not None:
        q = q.filter(
            Event.location_point.isnot(None),
            func.ST_Within(
                Event.location_point,
                geo_funcs.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326),
            ),
        )

    total = q.count()
    rows = (
        q.order_by(Event.source_published_at.desc().nullslast(), Event.ingested_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    event_ids = [r[0].id for r in rows]
    link_map = {}
    if event_ids:
        link_rows = (
            db.query(EventSourceLink.event_id, RawDocument.original_url)
            .join(RawDocument, EventSourceLink.raw_document_id == RawDocument.id)
            .filter(
                EventSourceLink.event_id.in_(event_ids),
                or_(
                    EventSourceLink.is_display_source == True,
                    EventSourceLink.relationship_type == "primary",
                ),
            )
        )
        seen = set()
        for eid, url in link_rows:
            if eid not in seen:
                link_map[eid] = url
                seen.add(eid)

    out = []
    for r in rows:
        event, layer_code, layer_name, sc_id, sc_name, tt_name, es_name, src_name = (
            r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]
        )
        lat, lon = None, None
        if event.location_point is not None:
            wkb = db.execute(select(geo_funcs.ST_AsText(event.location_point))).scalar()
            if wkb and wkb.startswith("POINT("):
                parts = wkb[6:-1].split()
                if len(parts) >= 2:
                    lon, lat = float(parts[0]), float(parts[1])
        out.append(
            {
                "id": event.id,
                "title": event.title,
                "layer_id": event.layer_id,
                "layer_code": layer_code,
                "layer_name": layer_name,
                "source_class_id": sc_id,
                "source_class_name": sc_name,
                "trust_tier_id": event.trust_tier_id,
                "trust_tier_name": tt_name,
                "evidence_status_id": event.evidence_status_id,
                "evidence_status_name": es_name,
                "source_name": src_name,
                "source_url": link_map.get(event.id),
                "source_published_at": event.source_published_at,
                "country_code": event.country_code,
                "region_code": event.region_code,
                "location_name": event.location_name,
                "lat": lat,
                "lon": lon,
                "summary_en": event.summary_en,
                "geographic_scope": event.geographic_scope,
            }
        )
    return out, total


def get_event_by_id(db: Session, event_id: UUID) -> dict | None:
    """Return full event dict for EventDetail or None."""
    event = (
        db.query(Event)
        .filter(Event.id == event_id, Event.visibility_status == "visible", Event.is_active == True)
        .first()
    )
    if not event:
        return None

    layer = db.query(Layer).filter(Layer.id == event.layer_id).first()
    provider = db.query(SourceProvider).filter(SourceProvider.id == event.primary_provider_id).first()
    source_class = db.query(SourceClass).filter(SourceClass.id == provider.source_class_id).first() if provider else None
    trust_tier = db.query(TrustTier).filter(TrustTier.id == event.trust_tier_id).first()
    evidence_status = db.query(EvidenceStatus).filter(EvidenceStatus.id == event.evidence_status_id).first()

    source_url = None
    link = (
        db.query(EventSourceLink)
        .join(RawDocument, EventSourceLink.raw_document_id == RawDocument.id)
        .filter(
            EventSourceLink.event_id == event_id,
            or_(
                EventSourceLink.is_display_source == True,
                EventSourceLink.relationship_type == "primary",
            ),
        )
        .first()
    )
    if link:
        raw = db.query(RawDocument).filter(RawDocument.id == link.raw_document_id).first()
        if raw:
            source_url = raw.original_url

    translations = (
        db.query(EventTranslation)
        .filter(EventTranslation.event_id == event_id)
        .all()
    )
    specialty_ids = [r.specialty_id for r in db.query(EventSpecialty).filter(EventSpecialty.event_id == event_id).all()]
    topic_ids = [r.topic_id for r in db.query(EventTopic).filter(EventTopic.event_id == event_id).all()]
    specialty_names = [r.name for r in db.query(Specialty).filter(Specialty.id.in_(specialty_ids)).all()] if specialty_ids else []
    topic_names = [r.name for r in db.query(Topic).filter(Topic.id.in_(topic_ids)).all()] if topic_ids else []

    return {
        "id": event.id,
        "title": event.title,
        "layer_id": event.layer_id,
        "layer_code": layer.code if layer else "",
        "layer_name": layer.name if layer else "",
        "source_class_id": provider.source_class_id if provider else 0,
        "source_class_name": source_class.name if source_class else "",
        "trust_tier_id": event.trust_tier_id,
        "trust_tier_name": trust_tier.name if trust_tier else "",
        "evidence_status_id": event.evidence_status_id,
        "evidence_status_name": evidence_status.name if evidence_status else "",
        "source_name": provider.name if provider else "",
        "source_url": source_url,
        "source_published_at": event.source_published_at,
        "event_occurred_at": event.event_occurred_at,
        "country_code": event.country_code,
        "region_code": event.region_code,
        "location_name": event.location_name,
        "geographic_scope": event.geographic_scope,
        "summary_en": event.summary_en,
        "relevance_label": event.relevance_label,
        "specialty_names": specialty_names,
        "topic_names": topic_names,
        "translations": [
            {"language_code": t.language_code, "translated_summary": t.translated_summary, "is_machine_translated": t.is_machine_translated}
            for t in translations
        ],
    }
