from worker.celery_app import app


@app.task
def normalize_raw_document(raw_document_id: str):
    """Normalize a raw document into canonical form. Placeholder for Phase 1."""
    return {"raw_document_id": raw_document_id, "status": "stub"}
