# Catálogo de Skills

Este documento lista las responsabilidades, puntos de integración y recomendaciones concretas por skill para el proyecto DevShelfApi.

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

## db-models

- Descripción: Modelado y operaciones CRUD con SQLAlchemy async.
- Responsabilidades: transacciones, índices, consultas eficientes.
- Archivos relevantes: [app/models/*.py](app/models), [app/db/session.py](app/db/session.py), [alembic/](alembic)
- Tests recomendados: tests de integración con Postgres.

## migrations

- Descripción: Alembic-driven migrations y workflow de despliegue.
- Responsabilidades: escribir migraciones, revisar `alembic/env.py`, CI check.

## deployment-docker

- Descripción: Containerización y orquestación.
- Responsabilidades: multi-stage builds, healthchecks, secrets via env.
- Archivos: [Dockerfile](Dockerfile), [docker-compose.yml](docker-compose.yml), `docker-compose.override.yml` (dev)

## testing-ci

- Descripción: Pruebas e integración continua.
- Responsabilidades: añadir matrix Postgres en CI, parallel tests, linting.
- Archivos: [tests/](tests), [.github/workflows/ci.yml](.github/workflows/ci.yml)

## observability

- Descripción: Logging, metrics, tracing, error reporting.
- Responsabilidades: exponer `/metrics`, inicializar OpenTelemetry, enviar errores a Sentry.
- Archivos: `internal/pipeline/orchestrator.py` (inspiración), `pkg/` (utilidades).

## orchestration-pipeline

- Descripción: Pipelines ETL/ML y orquestación.
- Responsabilidades: adapters, DLQ, idempotencia, escalado.
- Archivos: [internal/pipeline/orchestrator.py](internal/pipeline/orchestrator.py), [contracts/schemas.py](contracts/schemas.py)

## Plantillas y checklist por skill

- Cada skill debe incluir al menos: propósito, API pública (endpoints/funciones), tests, permisos necesarios, dependencias infra, y un runbook corto.

Ejemplo: `auth-jwt` checklist breve

- Crear tests para token expiry.
- Añadir rate-limiter en login.
- Definir rotation/revocation strategy.
