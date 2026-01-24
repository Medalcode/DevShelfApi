from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sa_update, delete as sa_delete
from app.api.deps import get_db, get_current_user
from app.schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate
from app.models.resource import Resource

router = APIRouter()


@router.post("/", response_model=ResourceRead, status_code=201)
async def create_resource(payload: ResourceCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    data = payload.model_dump()
    data["url"] = str(data.get("url"))
    obj = Resource(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/", response_model=List[ResourceRead])
async def list_resources(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resource).offset(skip).limit(limit))
    items = result.scalars().all()
    return items


@router.get("/{resource_id}", response_model=ResourceRead)
async def get_resource(resource_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return obj


@router.put("/{resource_id}", response_model=ResourceRead)
async def update_resource(resource_id: str, payload: ResourceUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{resource_id}", status_code=204)
async def delete_resource(resource_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    await db.delete(obj)
    await db.commit()
    return None
