from worker.celery_app import app


@app.task
def publish_canonical_event(raw_document_ids: list[str]):
    """Promote raw documents to canonical event. Placeholder for Phase 1."""
    return {"raw_document_ids": raw_document_ids, "status": "stub"}
