from worker.celery_app import app


@app.task
def summarize_event(event_id: str):
    """Generate AI summary for event. Placeholder for Phase 1."""
    return {"event_id": event_id, "status": "stub"}
