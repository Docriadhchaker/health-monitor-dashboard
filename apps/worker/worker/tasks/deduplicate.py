from worker.celery_app import app


@app.task
def deduplicate_events(batch_size: int = 100):
    """Run deduplication over recent events. Placeholder for Phase 1."""
    return {"batch_size": batch_size, "status": "stub"}
