import os

from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "healthmonitor",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "worker.tasks.ingest",
        "worker.tasks.normalize",
        "worker.tasks.geocode",
        "worker.tasks.summarize",
        "worker.tasks.translate",
        "worker.tasks.deduplicate",
        "worker.tasks.publish",
    ],
)
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.timezone = "UTC"
app.conf.enable_utc = True

# Beat schedule skeleton — periodic ingestion per feed (placeholder)
app.conf.beat_schedule = {
    "ingest-feeds-periodic": {
        "task": "worker.tasks.ingest.ingest_feed",
        "schedule": crontab(minute="*/30"),
        "args": ("placeholder-feed-id",),
    },
}
