from worker.celery_app import app


@app.task
def geocode_event(event_id: str):
    """Geocode event location. Placeholder for Phase 1."""
    return {"event_id": event_id, "status": "stub"}
