from celery import Celery
import os

from app.core.config import settings

# Broker/config: prefer REDIS_URL from env, fallback to settings
REDIS_URL = os.environ.get("REDIS_URL") or getattr(settings, "REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "devshelf",
    broker=REDIS_URL,
)

# Example: load config from env prefixed with CELERY_
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True)
def debug_task(self):
    print(f"Celery debug task. id: {self.request.id}")
