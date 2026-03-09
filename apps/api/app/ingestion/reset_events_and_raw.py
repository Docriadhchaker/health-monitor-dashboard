"""
Reset events and raw_documents so reseed + ingestion produce clean time semantics.
Run this before seed and ingest when you need 7d/30d to reflect real publication recency.
Order: clear event_translations, event_source_links, events, raw_documents; then run seed (demo with old dates), then ingest (WHO/ECDC with real dates).
"""
from __future__ import annotations

from app.db.session import SessionLocal
from app.models import Event, EventSourceLink, EventTranslation, RawDocument


def reset_events_and_raw_documents() -> dict:
    """
    Delete all event-related rows and raw_documents. Idempotent.
    Returns counts deleted.
    """
    db = SessionLocal()
    try:
        n_translations = db.query(EventTranslation).delete()
        n_links = db.query(EventSourceLink).delete()
        n_events = db.query(Event).delete()
        n_raw = db.query(RawDocument).delete()
        db.commit()
        return {
            "event_translations": n_translations,
            "event_source_links": n_links,
            "events": n_events,
            "raw_documents": n_raw,
        }
    finally:
        db.close()


def main() -> None:
    out = reset_events_and_raw_documents()
    print("Reset complete. Deleted:", out)
    print("Next: run seed, then run_who_ecdc_ingestion.")


if __name__ == "__main__":
    main()
