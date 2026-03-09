"""
Fetch and parse RSS feeds for WHO and ECDC.
Sanitize HTML in titles/summaries to plain text for event cards.
"""
from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from typing import Any

import feedparser
import httpx

RSS_FETCH_TIMEOUT = 30
SUMMARY_MAX_LENGTH = 600


def _strip_html_to_plain(text: str) -> str:
    """Strip HTML tags and decode entities; normalize whitespace. No raw HTML in UI."""
    if not text or not isinstance(text, str):
        return ""
    s = re.sub(r"<[^>]+>", " ", text)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# Official RSS URLs. WHO global feed (entity/news) returns 404; we use WHO AFRO as official fallback.
WHO_RSS_URL = "https://www.afro.who.int/rss/featured-news.xml"  # WHO Regional Office for Africa - Press releases
ECDC_RSS_URL = "https://www.ecdc.europa.eu/en/taxonomy/term/1307/feed"  # News / press releases


def _parse_published(entry: Any) -> datetime | None:
    """Parse entry published date to UTC datetime."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            from time import mktime
            from time import struct_time
            t = entry.published_parsed
            if isinstance(t, struct_time):
                ts = mktime(t)
                return datetime.fromtimestamp(ts, tz=timezone.utc)
        except (TypeError, OSError):
            pass
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        try:
            from time import mktime
            from time import struct_time
            t = entry.updated_parsed
            if isinstance(t, struct_time):
                ts = mktime(t)
                return datetime.fromtimestamp(ts, tz=timezone.utc)
        except (TypeError, OSError):
            pass
    return None


def fetch_rss(url: str) -> list[dict[str, Any]]:
    """
    Fetch RSS from url and return list of normalized items.
    Each item: title, link, summary, source_published_at (datetime|None), raw_payload (for raw_documents).
    """
    with httpx.Client(timeout=RSS_FETCH_TIMEOUT) as client:
        resp = client.get(url)
        resp.raise_for_status()
        text = resp.text
    parsed = feedparser.parse(text)
    items = []
    for entry in parsed.entries:
        link = (entry.get("link") or "").strip()
        if not link:
            continue
        raw_title = (entry.get("title") or "").strip() or "Untitled"
        raw_summary = (entry.get("summary") or entry.get("description") or "").strip()
        title = _strip_html_to_plain(raw_title) or "Untitled"
        summary = _strip_html_to_plain(raw_summary)
        if summary and len(summary) > SUMMARY_MAX_LENGTH:
            summary = summary[: SUMMARY_MAX_LENGTH - 3].rsplit(" ", 1)[0] + "..."
        published = _parse_published(entry)
        items.append({
            "title": title,
            "link": link,
            "summary": summary or None,
            "source_published_at": published,
            "raw_payload": {
                "title": raw_title,
                "link": link,
                "summary": raw_summary,
                "published": entry.get("published") or entry.get("updated"),
            },
        })
    return items
