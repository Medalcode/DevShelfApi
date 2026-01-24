# Bitácora del desarrollo

Fecha: 24 de enero de 2026

Resumen ejecutivo
------------------
- Proyecto: Biblioteca de Recursos para Programadores (API REST)
- Stack: FastAPI, Uvicorn, SQLAlchemy (async), Pydantic v2, Alembic, Docker, Postgres (docker-compose), pytest.
- Objetivo: Reformular el proyecto y crear un scaffold escalable con autenticación JWT, pruebas, migraciones y CI.

Qué se desarrolló
------------------

1) Estructura del proyecto
- `app/` paquete con módulos: `core`, `db`, `models`, `schemas`, `api/v1`, `services`.
- `tests/` con pruebas de integración para root, auth y CRUD de recursos.
- Archivos de entorno y despliegue: `Dockerfile`, `docker-compose.yml`, `.env.example`, `.dockerignore`.
- Alembic: `alembic/` con `env.py` y versión inicial `0001_initial.py`.

2) Autenticación
- JWT usando `python-jose`.
- Hashing de contraseñas con `passlib` y `pbkdf2_sha256` (por compatibilidad en el entorno).
- Endpoints: registro (`/api/v1/auth/register`), token (`/api/v1/auth/token`) y dependencia `get_current_user` para rutas protegidas.

3) Modelos y esquemas
- Modelos SQLAlchemy asíncronos: `User` y `Resource`.
- Esquemas Pydantic v2 para `User`, `Token`, `Resource` con `model_config = ConfigDict(from_attributes=True)`.

4) Rutas y servicios
- Rutas CRUD para `resources` (lista, detalle, crear, actualizar, borrar).
- Rutas de autenticación en `api/v1/routes/auth.py`.
- Lógica de negocio mínima en `services/auth.py` para creación y autenticación de usuarios.

5) Base de datos y migraciones
- Sesión asíncrona configurada en `app/db/session.py` usando `DATABASE_URL`.
- Alembic preparado para migraciones (esqueleto y primera versión).

6) Pruebas
- `pytest` + `pytest-asyncio` + `httpx` (ASGITransport) para pruebas ASGI.
- Pruebas incluidas: `tests/test_root.py`, `tests/test_auth.py`, `tests/test_resources_crud.py`.
- Estado actual: pruebas locales ejecutadas correctamente (3 passed).

7) CI y despliegue
- Workflow de GitHub Actions en `.github/workflows/ci.yml` para ejecutar tests en PRs/push.
- `docker-compose.yml` para ambiente de desarrollo con Postgres.

Problemas encontrados y soluciones
----------------------------------
- Migración a Pydantic v2: reemplazo de patrones antiguos (`.dict()`, `BaseSettings`) por `model_dump()` y `pydantic-settings`/`ConfigDict`.
- Dependencias faltantes en el entorno de desarrollo: `aiosqlite`, `pytest-asyncio`, `pydantic[email]`, `python-jose`, `passlib`, `cryptography`, entre otras — se añadieron a `requirements.txt`.
- Problemas con `bcrypt` en el entorno: se cambió a `pbkdf2_sha256` para evitar dependencias nativas.
- Errores de binding al insertar `HttpUrl` en la DB: se convirtió a `str` antes de persistir.
- Creación de tablas durante pruebas: se usa un lifespan/creación explícita de tablas al inicio de pruebas para evitar errores de tablas faltantes.

Cambios principales (archivos y roles)
-------------------------------------
- `app/main.py`: punto de entrada ASGI y lifespan para startup.
- `app/core/config.py`: Settings con `pydantic-settings`.
- `app/core/security.py`: utilidades JWT y hash.
- `app/db/session.py`: configuración de engine y `AsyncSession`.
- `app/models/*`: modelos `User`, `Resource`, `Base`.
- `app/schemas/*`: Pydantic v2 schemas.
- `app/api/v1/routes/*`: rutas `auth` y `resources`.
- `app/services/auth.py`: lógica de user creation y auth.
- `alembic/`: configuración de migraciones y primera versión.
- `tests/`: pruebas automatizadas.
- `Dockerfile`, `docker-compose.yml`: contenedores de app y bd.
- `.github/workflows/ci.yml`: pipeline de CI para tests.

Estado actual y próximos pasos recomendados
-----------------------------------------
- Estado: scaffold completo, pruebas locales pasando, commit local realizado.
- Recomendado:
  - Rotar `SECRET_KEY` y gestionarla desde variables de entorno seguras.
  - Completar documentación de migraciones y comandos Alembic.
  - Probar pipeline CI remoto (push/PR) y ajustar si el runner difiere del entorno local.
  - Añadir más pruebas y casos de borde, validación de esquemas y manejo de errores.

Notas finales
------------
Este documento pretende servir como registro de decisiones técnicas y de la actividad realizada hasta la fecha indicada arriba. Si quieres, puedo ampliar cualquier sección (por ejemplo: exportar diffs de commits, checklist para producción, o un manual de despliegue).
