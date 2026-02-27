import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    username = f"user_{uuid.uuid4().hex[:8]}"
    payload = {"username": username, "email": f"{username}@example.com", "password": "secret"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # ensure tables exist for tests
        from app.db.session import async_engine, Base

        import asyncio

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        r = await ac.post("/api/v1/auth/register", json=payload)
        assert r.status_code == 201
        data = r.json()
        assert data["username"] == username

        # login
        r2 = await ac.post("/api/v1/auth/token", json=payload)
        assert r2.status_code == 200
        token_data = r2.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
