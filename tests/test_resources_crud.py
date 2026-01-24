import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_resources_crud():
    username = f"user_{uuid.uuid4().hex[:8]}"
    user_payload = {"username": username, "email": f"{username}@example.com", "password": "secret"}
    resource_payload = {"title": "Test Resource", "description": "desc", "url": "https://example.com", "type": "article"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # ensure tables exist for tests
        from app.db.session import async_engine
        from app.models.base import Base

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # register and obtain token
        r = await ac.post("/api/v1/auth/register", json=user_payload)
        assert r.status_code == 201
        r2 = await ac.post("/api/v1/auth/token", json=user_payload)
        assert r2.status_code == 200
        token = r2.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # create resource (protected)
        r3 = await ac.post("/api/v1/resources/", json=resource_payload, headers=headers)
        assert r3.status_code == 201
        created = r3.json()
        resource_id = created["id"]

        # list resources
        r4 = await ac.get("/api/v1/resources/")
        assert r4.status_code == 200
        assert any(item["id"] == resource_id for item in r4.json())

        # get resource
        r5 = await ac.get(f"/api/v1/resources/{resource_id}")
        assert r5.status_code == 200

        # update resource (protected)
        r6 = await ac.put(f"/api/v1/resources/{resource_id}", json={"title": "Updated"}, headers=headers)
        assert r6.status_code == 200
        assert r6.json()["title"] == "Updated"

        # delete resource (protected)
        r7 = await ac.delete(f"/api/v1/resources/{resource_id}", headers=headers)
        assert r7.status_code == 204
