# DevShelfApi

API escalable para gestión y compartición de recursos técnicos para programadores.

![Status](https://img.shields.io/badge/Status-Beta-blue) ![Python](https://img.shields.io/badge/Python-3.12-yellow)

## Resumen

DevShelfApi es una API construida con **FastAPI**, **SQLAlchemy async** y **Alembic**. Diseñada con arquitectura de Pipes & Filters, soporte para workers (Celery + Redis) y lista para Kubernetes.

## Estructura

```
app/
├── api/v1/routes/      # Endpoints HTTP: auth.py, resources.py
├── core/               # Lógica central compartida
│   ├── config.py       # Settings (pydantic)
│   ├── logging.py      # Logger estructurado JSON
│   ├── security.py     # JWT, hashing
│   ├── pipeline.py     # Orquestador del pipeline de datos (TASKS.md PIPE-001)
│   └── workers.py      # Celery app + tareas background
├── db/
│   └── session.py      # Engine async + Base declarativa (SQLAlchemy)
├── models/             # Modelos ORM: user.py, resource.py
├── schemas/            # Schemas Pydantic: user.py, resource.py
├── services/           # Lógica de negocio: auth.py
└── main.py             # Entrypoint FastAPI
contracts/
└── schemas.py          # DTOs inmutables: RawDocument, FeatureSet, PredictionResult
alembic/                # Migraciones de base de datos
docs/
├── agent.md            # Agente Generalista: roles y runbooks operacionales
└── skills.md           # Catálogo de Super-Skills paramétricas
tests/                  # test_auth.py, test_resources_crud.py, test_root.py
```

## Inicio rápido

### Docker (recomendado)

```bash
docker-compose up --build
```

El override de desarrollo (`docker-compose.override.yml`) activa Redis para Celery automáticamente.

### Local (Windows PowerShell)

```powershell
python -m venv .venv
. .venv\Scripts\Activate
pip install -r requirements.txt
alembic upgrade head
pytest -q
```

## Migraciones

> ⚠️ **Nunca usar `Base.metadata.create_all` en producción.** Las migraciones se gestionan exclusivamente con Alembic.

```bash
alembic upgrade head      # aplicar migraciones
alembic downgrade -1      # rollback una revisión
```

## Documentación operacional

| Documento | Contenido |
|---|---|
| [docs/agent.md](docs/agent.md) | Agente Generalista con 4 roles: `api-operator`, `db-admin`, `security-auditor`, `infra-operator` |
| [docs/skills.md](docs/skills.md) | 5 Super-Skills paramétricas: `api-http`, `auth-jwt`, `database`, `deployment-docker`, `quality-ops` |
| [ARQUITECTURA.md](ARQUITECTURA.md) | Diagrama de pipeline y matriz de responsabilidades por módulo |
| [TASKS.md](TASKS.md) | Backlog priorizado: ARCH-001/002, PIPE-001/002, API-001, OBS-001 |

## Observabilidad

- Logs estructurados JSON via `app/core/logging.py`
- Prometheus (`/metrics`), OpenTelemetry y Sentry — ver `docs/skills.md#quality-ops`

## Próximos pasos

- Helm chart para Kubernetes (readiness/liveness, HPA, secrets)
- Implementar `DummyStrategy` para inferencia local (TASKS.md PIPE-002)
- CI job que detecte migraciones de Alembic sin aplicar
