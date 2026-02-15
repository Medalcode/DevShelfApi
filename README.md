# DevShelfApi

Proyecto API escalable para gestión y compartición de recursos técnicos.

![Status](https://img.shields.io/badge/Status-Beta-blue) ![Python](https://img.shields.io/badge/Python-3.11-yellow)

## Resumen

DevShelfApi es una API construida con FastAPI, SQLAlchemy async y Alembic para gestionar recursos (links, descripciones y metadatos). Está preparada para evolucionar hacia un despliegue en Kubernetes, con soporte para workers (Celery + Redis) y observabilidad.

## Estructura relevante

- Entrypoint: [app/main.py](app/main.py)
- Rutas API v1: [app/api/v1/routes](app/api/v1/routes)
- Modelos: [app/models](app/models)
- DB session: [app/db/session.py](app/db/session.py)
- Migrations: [alembic/](alembic)

## Documentación añadida

- Agregados: [docs/agent.md](docs/agent.md) (runbook y operaciones) y [docs/skills.md](docs/skills.md) (catálogo de skills y responsabilidades).

## Ejecutar localmente (desarrollo)

Recomendado usar el override de desarrollo para incluir Redis y worker:

```bash
docker-compose up --build
# o con override (usa docker-compose.override.yml automáticamente cuando existe)
docker-compose up --build
```

Crear entorno virtual e instalar deps:

```powershell
python -m venv .venv
. .venv\Scripts\Activate
pip install -r requirements.txt
pytest -q
```

## Observabilidad y background

- Se añadieron plantillas: `app/celery_app.py` y `app/core/logging.py`.
- Se recomienda instrumentar la app con Prometheus + OpenTelemetry + Sentry en producción.

## Contribuir

- Añade issues por skill usando `docs/skills.md` como guía.
- Evitar usar `Base.metadata.create_all` en producción; usar Alembic (`alembic upgrade head`).

## Próximos pasos

- Preparar Helm chart para Kubernetes y CI jobs que verifiquen migraciones.
- Instrumentar métricas y tracing; añadir tasks de Celery y pruebas de integración.
