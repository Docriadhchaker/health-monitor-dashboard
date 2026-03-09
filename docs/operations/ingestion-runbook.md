# Ingestion Runbook

- **Scheduled ingestion:** Celery Beat triggers `ingest_feed` per source feed at configured intervals.
- **Manual run:** Invoke worker task `ingest_feed` with feed_id, or run `ingestion/jobs/run_ingestion.py` (when implemented).
- **Monitoring:** Check `ingestion_runs` table for status, `records_fetched` / `records_promoted`, and `error_message` on failure.
- **Reprocessing:** Use `event_change_log` and raw_documents for traceability; re-run summarization/translation tasks when needed.
