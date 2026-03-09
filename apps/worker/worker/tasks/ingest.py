from worker.celery_app import app


@app.task
def ingest_feed(feed_id: str):
    """Poll a source feed and store raw documents. Stub for MVP scaffold."""
    return {"feed_id": feed_id, "status": "stub"}
