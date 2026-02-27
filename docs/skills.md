# Catálogo de Skills

Este documento lista las responsabilidades, puntos de integración y recomendaciones concretas por skill para el proyecto DevShelfApi.

> **Principio de Reutilización:** Antes de añadir una nueva skill, verifica si una skill existente acepta un parámetro `scope` extra que cubra el caso de uso. No se crea una skill nueva si el 80% de la lógica ya existe.

## api-http

- Descripción: Operaciones CRUD, validación, paginación y routers FastAPI.
- Responsabilidades: Añadir endpoints, documentar contratos, validar inputs, implementar paginación eficiente.
- Archivos relevantes: [app/main.py](app/main.py), [app/api/v1/routes/resources.py](app/api/v1/routes/resources.py), [app/api/v1/routes/auth.py](app/api/v1/routes/auth.py)
- Tests: `tests/test_resources_crud.py`.
- Infra requerida: none adicional.

## auth-jwt

- Descripción: Flujo de registro/login, JWT creation/validation, password hashing.
- Responsabilidades: expiración y refresh tokens, revocación, rate-limiting, hardening.
- Archivos relevantes: [app/core/security.py](app/core/security.py), [app/services/auth.py](app/services/auth.py), [app/api/deps.py](app/api/deps.py)
- Tests recomendados: tests de expiración, refresh token flow, revocación.

## database

> **Super-Skill** — parámetro `scope: models | migrations | both` (default: `both`)

- Descripción: Modelado SQLAlchemy async y ciclo de vida de migraciones Alembic. Estas responsabilidades son inseparables: un cambio de modelo siempre produce una migración.
- Responsabilidades por `scope`:
  - `models`: diseño de entidades, relaciones, índices, consultas eficientes, transacciones.
  - `migrations`: escritura de scripts Alembic, revisión de `alembic/env.py`, CI check de migraciones pendientes.
  - `both` (default): todo lo anterior de forma coordinada.
- Archivos relevantes: [app/models/*.py](app/models), [app/db/session.py](app/db/session.py), [alembic/](alembic), [alembic/env.py](alembic/env.py)
- Tests recomendados: tests de integración con Postgres (modelos) + test CI que detecte migraciones sin aplicar.

## deployment-docker

- Descripción: Containerización y orquestación.
- Responsabilidades: multi-stage builds, healthchecks, secrets via env.
- Archivos: [Dockerfile](Dockerfile), [docker-compose.yml](docker-compose.yml), `docker-compose.override.yml` (dev)

## quality-ops

> **Super-Skill** — parámetro `scope: testing | observability | both` (default: `both`)

- Descripción: Calidad operacional end-to-end: pruebas automatizadas, CI y visibilidad del sistema en producción. Se unifican aquí porque comparten el mismo ciclo de feedback y las mismas pipelines de CI.
- Responsabilidades por `scope`:
  - `testing`: matrix Postgres en CI, tests paralelos, linting, smoke tests post-deploy.
  - `observability`: logs estructurados JSON, `/metrics` para Prometheus, inicialización de OpenTelemetry, envío de errores a Sentry, propagación de `trace_id` a tareas Celery.
  - `both` (default): CI verde + sistema observable en producción.
- Archivos relevantes: [tests/](tests), [.github/workflows/ci.yml](.github/workflows/ci.yml), `pkg/` (utilidades de logging/tracing)
- Nota sobre pipeline: la lógica de orquestación (adaptadores, DLQ, idempotencia) está documentada en [ARQUITECTURA.md](../ARQUITECTURA.md) §1 y en TASKS.md PIPE-001. No se duplica aquí.

## Plantilla y checklist por skill

Cada skill (incluyendo Super-Skills) debe incluir:

- **Propósito**: qué problema resuelve.
- **Parámetro `scope`** (si aplica): valores posibles y comportamiento por defecto.
- **API pública**: endpoints o funciones expuestas.
- **Tests**: qué debe cubrir el test suite.
- **Dependencias infra**: servicios externos requeridos (Redis, Postgres, etc.).
- **Runbook corto**: pasos de diagnóstico en caso de fallo.

### Ejemplo: `auth-jwt` checklist

- Crear tests para token expiry y refresh flow.
- Añadir rate-limiter en `/token` y `/register`.
- Definir rotation/revocation strategy (ver `app/core/security.py`).
