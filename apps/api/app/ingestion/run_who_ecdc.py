"""
Run real ingestion for WHO and ECDC RSS feeds.
Rerunnable: skips duplicate raw_documents and events.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import IngestionRun, SourceFeed, SourceProvider
from app.ingestion.rss import fetch_rss, WHO_RSS_URL, ECDC_RSS_URL
from app.ingestion.promote import process_feed_run


# Use these when feed.endpoint_url is a placeholder (e.g. example.com)
RSS_URL_BY_SLUG = {
    "who": WHO_RSS_URL,
    "ecdc": ECDC_RSS_URL,
}


def _rss_url_for_feed(feed: SourceFeed, provider_slug: str) -> str:
    if feed.endpoint_url and "example.com" not in feed.endpoint_url:
        return feed.endpoint_url
    return RSS_URL_BY_SLUG.get(provider_slug, feed.endpoint_url)


def run_who_ecdc_ingestion(db: Session | None = None) -> dict:
    """
    Fetch WHO and ECDC RSS, create raw_documents and promote to events.
    If db is None, creates a new session and commits; otherwise uses caller's session.
    Returns summary: { who: { run_id, fetched, inserted, promoted }, ecdc: { ... } }.
    """
    own_session = db is None
    if own_session:
        db = SessionLocal()
    try:
        feeds = (
            db.query(SourceFeed)
            .join(SourceProvider, SourceFeed.provider_id == SourceProvider.id)
            .filter(SourceProvider.slug.in_(["who", "ecdc"]))
            .all()
        )
        result = {}
        for feed in feeds:
            provider = db.query(SourceProvider).filter(SourceProvider.id == feed.provider_id).first()
            slug = provider.slug if provider else None
            if slug not in ("who", "ecdc"):
                continue
            url = _rss_url_for_feed(feed, slug)
            run_id = uuid.uuid4()
            started = datetime.now(timezone.utc)
            db.add(
                IngestionRun(
                    id=run_id,
                    source_feed_id=feed.id,
                    status="running",
                    started_at=started,
                    records_fetched=0,
                    records_inserted=0,
                    records_promoted=0,
                )
            )
            db.flush()
            try:
                items = fetch_rss(url)
            except Exception as e:
                run = db.query(IngestionRun).filter(IngestionRun.id == run_id).first()
                if run:
                    run.status = "failed"
                    run.finished_at = datetime.now(timezone.utc)
                    run.error_message = str(e)[:500]
                result[slug] = {"run_id": str(run_id), "error": str(e), "fetched": 0, "inserted": 0, "promoted": 0}
                continue
            inserted, promoted = process_feed_run(db, feed, run_id, items)
            finished = datetime.now(timezone.utc)
            run = db.query(IngestionRun).filter(IngestionRun.id == run_id).first()
            if run:
                run.status = "success"
                run.finished_at = finished
                run.records_fetched = len(items)
                run.records_inserted = inserted
                run.records_promoted = promoted
            result[slug] = {
                "run_id": str(run_id),
                "fetched": len(items),
                "inserted": inserted,
                "promoted": promoted,
            }
        if own_session:
            db.commit()
        return result
    finally:
        if own_session and db:
            db.close()


def main() -> None:
    """CLI entrypoint."""
    out = run_who_ecdc_ingestion()
    print("WHO/ECDC ingestion complete:", out)


if __name__ == "__main__":
    main()
