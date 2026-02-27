# Agente Generalista: DevShelf Operator

> **Principio de Densidad:** Este es el único agente del proyecto. No se crean agentes adicionales si el contexto puede resolverse añadiendo un rol o capacidad aquí.

## Propósito

Agente único responsable de ejecutar, mantener, escalar y diagnosticar la API DevShelf. Agrupa modos de operación como **roles** en lugar de crear archivos de agente separados.

## Roles

| Rol | Responsabilidad principal | Skill asociada |
|---|---|---|
| `api-operator` | Endpoints HTTP, validación, contratos | [`api-http`](skills.md#api-http) |
| `db-admin` | Modelos, migraciones y sesiones DB | [`database`](skills.md#database) (`scope: both`) |
| `security-auditor` | JWT, tokens, rate-limiting, hardening | [`auth-jwt`](skills.md#auth-jwt) |
| `infra-operator` | Docker, CI, observabilidad, workers Celery | [`deployment-docker`](skills.md#deployment-docker), [`quality-ops`](skills.md#quality-ops) |

## Capacidades comunes (todos los roles)

- Ejecutar tests: `pytest -q` (ver `tests/`).
- Ejecutar migraciones Alembic: `alembic upgrade head`.
- Levantar entorno local con Docker Compose: `docker-compose up --build`.
- Diagnóstico básico: logs, healthchecks y métricas.
- Arquitectura del pipeline y orquestación: ver [ARQUITECTURA.md](../ARQUITECTURA.md) §1 y TASKS.md PIPE-001.

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

## Rol: `security-auditor` — Checklist

> Ver skill [`auth-jwt`](skills.md#auth-jwt) para la implementación detallada. No se duplica aquí.

- Verificar que `SECRET_KEY` no tenga valores por defecto en `app/core/config.py`.
- Confirmar refresh tokens + revocación implementados.
- Auditar rate-limiting en `/token` y `/register`.

## Rol: `infra-operator` — Checklist

> Ver skills [`deployment-docker`](skills.md#deployment-docker) y [`quality-ops`](skills.md#quality-ops) (`scope: both`) para detalles.

- Logs estructurados (JSON) y niveles por entorno.
- `/metrics` expuesto para Prometheus scrape.
- OpenTelemetry inicializado en startup; `trace_id` propagado a tareas Celery (`app/celery_app.py`).
- Errores enviados a Sentry en producción.
- Redis en `docker-compose.override.yml` para Workers locales.

## Procedimiento de verificación post-deploy

1. Verificar endpoints básicos y autenticación.
2. Verificar `/metrics` y que Prometheus scrapee la app.
3. Ejecutar job de smoke tests (tests críticos).

## Siguientes pasos recomendados

- Añadir Helm chart y manifests Kubernetes con readiness/liveness, HPA y secrets.
- Añadir job de CI que verifique migraciones pendientes.
- Implementar observabilidad completa y pruebas de carga.
