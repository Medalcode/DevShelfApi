"""
Celery Workers — movido desde app/celery_app.py

Configuración del worker de tareas en background.
Ver docs/agent.md § Rol: infra-operator para runbook de Redis.
"""
import os

from celery import Celery

from app.core.config import settings

# Broker: prefer REDIS_URL from env, fallback to settings
REDIS_URL = os.environ.get("REDIS_URL") or getattr(settings, "REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("devshelf", broker=REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Celery debug task. id: {self.request.id}")
