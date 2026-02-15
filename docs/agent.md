# Agent: Operaciones y Runbook

## Propósito

Este agente documenta las responsabilidades operacionales para ejecutar, mantener y escalar la API DevShelf (DevShelfApi).

## Alcance

- Endpoints y surface HTTP: ver [app/main.py](app/main.py) y [app/api/v1](app/api/v1)
- Autenticación y seguridad: [app/core/security.py](app/core/security.py)
- Base de datos y migraciones: [app/db/session.py](app/db/session.py), [alembic/env.py](alembic/env.py)
- Despliegue: Docker / Kubernetes (Helm)
- Observabilidad: métricas, tracing, logging
- Workers: integración con Celery + Redis

## Capacidades del agente

- Ejecutar tests: `pytest -q` (ver `tests/`).
- Ejecutar migraciones Alembic: `alembic upgrade head`.
- Levantar entorno local con Docker Compose: `docker-compose up --build`.
- Diagnóstico básico: logs, healthchecks y métricas.

## Comandos útiles

```bash
docker-compose up --build
pytest -q
alembic upgrade head
```

En Windows PowerShell:

```powershell
python -m venv .venv
. .venv\\Scripts\\Activate
pip install -r requirements.txt
pytest -q
```

## Runbook rápido (deploy seguro de DB)

1. No ejecutar `Base.metadata.create_all` en producción. Usar Alembic para migraciones (ver [alembic/env.py](alembic/env.py)).
2. Ejecutar `alembic upgrade head` en una job de deploy previo al cambio de imagen.
3. Verificar health/readiness endpoints.
4. En caso de rollback: ejecutar `alembic downgrade` a la revisión conocida y coordinar con la aplicación.

## Checklist de producción

- Secrets: provisionar `DATABASE_URL`, `SECRET_KEY`, `SENTRY_DSN` fuera del repositorio (Vault/Secrets Manager/Sealed Secrets).
- Healthchecks: añadir `/health` y `/ready` (DB, Redis).
- DB pooling y retries: ajustar `app/db/session.py` para producción.
- Observabilidad: Prometheus + OpenTelemetry + Sentry.
- Workers: Celery + Redis para tareas en background.

## Seguridad y tokens

- Evitar valores por defecto de `SECRET_KEY` en `app/core/config.py`.
- Implementar refresh tokens y revocación para tokens JWT.
- Añadir rate-limiting en endpoints sensibles (`/token`, `/register`).

## Observabilidad (resumen)

- Logs estructurados (JSON) y niveles por entorno.
- Exponer `/metrics` para Prometheus.
- Inicializar OpenTelemetry en startup y propagar contexto a Celery tasks.
- Enviar errores a Sentry en producción.

## Workers

- Plantilla de Celery en `app/celery_app.py`.
- Añadir `redis` al `docker-compose` de desarrollo (ver `docker-compose.override.yml`).

## Procedimiento de verificación post-deploy

1. Verificar endpoints básicos y autenticación.
2. Verificar `/metrics` y que Prometheus scrapee la app.
3. Ejecutar job de smoke tests (tests críticos).

## Siguientes pasos recomendados

- Añadir Helm chart y manifests Kubernetes con readiness/liveness, HPA y secrets.
- Añadir job de CI que verifique migraciones pendientes.
- Implementar observabilidad completa y pruebas de carga.
