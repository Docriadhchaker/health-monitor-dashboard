from worker.celery_app import app


@app.task
def translate_event_summary(event_id: str, target_lang: str = "fr"):
    """Translate event summary. Placeholder for Phase 1."""
    return {"event_id": event_id, "target_lang": target_lang, "status": "stub"}
