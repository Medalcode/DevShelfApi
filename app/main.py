from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.config import settings
from app.db.session import async_engine, Base  # Base consolidado en session.py
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # NOTA: NO usar Base.metadata.create_all en producción.
    # Las migraciones se gestionan exclusivamente con Alembic (ver agent.md Runbook).
    # En desarrollo puro: descomentar la línea de abajo solo si NO usas Alembic.
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)


app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a la API de la Biblioteca de Recursos para Programadores!"}
