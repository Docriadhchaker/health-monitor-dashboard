"""
Normalize RSS items into raw_documents and promote to canonical events.
Respects unique (source_feed_id, original_url); avoids duplicate events.
Derives region from source (WHO AFRO -> AFRICA, ECDC -> EUROPE) and applies
region-level centroid fallback so items appear on map without fabricating city coords.
"""
from __future__ import annotations

import hashlib
import uuid

from geoalchemy2.elements import WKTElement
from sqlalchemy.orm import Session

from app.models import (
    Event,
    EventSourceLink,
    EvidenceStatus,
    RawDocument,
    SourceFeed,
    SourceProvider,
    TrustTier,
)

# Region-level centroids (lon, lat) for map fallback when no precise coords. No city-level fabrication.
REGION_CENTROIDS = {
    "EUROPE": (10.0, 50.0),
    "AFRICA": (20.0, 0.0),
    "AMERICAS": (-75.0, -15.0),
    "ASIA": (100.0, 34.0),
    "MENA": (40.0, 25.0),
    "OCEANIA": (135.0, -25.0),
    "WORLD": (20.0, 20.0),
}

# Extensions and path segments that indicate non-article / media assets (skip promotion).
_ASSET_EXTENSIONS = frozenset(
    (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".bmp", ".tiff", ".pdf")
)
_ASSET_PATH_SEGMENTS = ("/logo", "/image/", "/images/", "/media/", "/assets/", "/static/")


def _is_low_quality_item(item: dict) -> bool:
    """Return True if the item should be skipped (logo, placeholder, asset URL, etc.)."""
    title = (item.get("title") or "").strip()
    link = (item.get("link") or "").strip()

    if len(title) < 3:
        return True
    title_lower = title.lower()
    if "_logo" in title_lower or "logo." in title_lower or title_lower.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico")):
        return True

    try:
        from urllib.parse import urlparse
        parsed = urlparse(link)
        path = (parsed.path or "").lower()
    except Exception:
        return True
    if not path or path == "/":
        return True
    if any(path.endswith(ext) for ext in _ASSET_EXTENSIONS):
        return True
    if any(seg in path for seg in _ASSET_PATH_SEGMENTS):
        return True
    return False


def _id_by_code(db: Session, model: type, code_attr: str, code_val: str) -> int | None:
    row = db.query(model).filter(getattr(model, code_attr) == code_val).first()
    return row.id if row else None


def _region_and_point_for_provider(db: Session, provider_id: uuid.UUID, feed: SourceFeed) -> tuple[str | None, object]:
    """Derive region_code and location_point from source. WHO AFRO -> AFRICA, ECDC -> EUROPE. Point = region centroid."""
    provider = db.query(SourceProvider).filter(SourceProvider.id == provider_id).first()
    slug = provider.slug if provider else None
    region_code = None
    if slug == "ecdc":
        region_code = "EUROPE"
    elif slug == "who":
        region_code = "AFRICA"  # WHO AFRO feed
    if not region_code:
        return None, None
    centroid = REGION_CENTROIDS.get(region_code)
    if centroid:
        lon, lat = centroid
        return region_code, WKTElement(f"POINT({lon} {lat})", srid=4326)
    return region_code, None


def process_feed_run(
    db: Session,
    feed: SourceFeed,
    run_id: uuid.UUID,
    items: list[dict],
) -> tuple[int, int]:
    """
    For each item: get or create RawDocument; if new or no event yet, create Event + EventSourceLink.
    Sets region_code and location_point from source (region-level centroid) so items are map-visible.
    Returns (records_inserted, records_promoted).
    """
    provider_id = feed.provider_id
    feed_id = feed.id
    layer_id = feed.default_layer_id
    evidence_id = _id_by_code(db, EvidenceStatus, "code", "SURVEILLANCE_REPORT") or 1
    trust_tier_id = _id_by_code(db, TrustTier, "code", "HIGH") or 1
    region_code, location_point = _region_and_point_for_provider(db, provider_id, feed)
    geographic_scope = "regional" if region_code else "global"

    records_inserted = 0
    records_promoted = 0

    for item in items:
        if _is_low_quality_item(item):
            continue
        link = item["link"]
        title = item["title"]
        summary = item.get("summary")
        source_published_at = item.get("source_published_at")
        raw_payload = item.get("raw_payload") or {"title": title, "link": link}

        existing_raw = (
            db.query(RawDocument)
            .filter(
                RawDocument.source_feed_id == feed_id,
                RawDocument.original_url == link,
            )
            .first()
        )

        if existing_raw:
            raw_id = existing_raw.id
            # Check if event already exists for this raw document
            has_event = (
                db.query(EventSourceLink)
                .filter(EventSourceLink.raw_document_id == raw_id)
                .first()
            ) is not None
            if has_event:
                continue
            # Promote existing raw_doc to event
            raw_doc = existing_raw
        else:
            content_hash = hashlib.sha256(link.encode()).hexdigest()[:128]
            raw_doc = RawDocument(
                id=uuid.uuid4(),
                ingestion_run_id=run_id,
                source_feed_id=feed_id,
                provider_id=provider_id,
                original_title=title,
                original_url=link,
                raw_payload_json=raw_payload,
                content_hash=content_hash,
                source_published_at=source_published_at,
                parsing_status="parsed",
            )
            db.add(raw_doc)
            db.flush()
            records_inserted += 1

        event_id = uuid.uuid4()
        geo_precision = "region_fallback" if location_point and region_code else "global"
        db.add(
            Event(
                id=event_id,
                layer_id=layer_id,
                primary_provider_id=provider_id,
                primary_raw_document_id=raw_doc.id,
                evidence_status_id=evidence_id,
                trust_tier_id=trust_tier_id,
                title=title,
                summary_en=summary,
                source_published_at=source_published_at,
                geographic_scope=geographic_scope,
                region_code=region_code,
                location_point=location_point,
                geo_precision=geo_precision,
                visibility_status="visible",
                is_active=True,
            )
        )
        db.flush()
        db.add(
            EventSourceLink(
                id=uuid.uuid4(),
                event_id=event_id,
                raw_document_id=raw_doc.id,
                provider_id=provider_id,
                relationship_type="primary",
                is_display_source=True,
            )
        )
        records_promoted += 1

    return records_inserted, records_promoted
