# Biblioteca de Recursos para Programadores — API (FastAPI scaffold)

Scaffold inicial de una API RESTful con FastAPI, SQLAlchemy (async) y Alembic.

Run rápido (Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=sqlite+aiosqlite:///./dev.db
uvicorn app.main:app --reload
```

Docs interactiva: http://127.0.0.1:8000/docs
 
Docker (development)
---------------------
Build and run the app with Postgres using docker-compose:

```bash
docker compose build
docker compose up
```

The service exposes the API at http://127.0.0.1:8000 and Postgres on port 5432.

If you prefer running locally without Docker, set `DATABASE_URL` to `sqlite+aiosqlite:///./dev.db`.
