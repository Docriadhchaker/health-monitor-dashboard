"""
Real ingestion for WHO and ECDC RSS feeds.
Fetch items, normalize to raw_documents, promote to canonical events.
"""

from app.ingestion.run_who_ecdc import run_who_ecdc_ingestion

__all__ = ["run_who_ecdc_ingestion"]
