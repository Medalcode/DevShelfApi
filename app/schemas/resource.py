from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime


class ResourceBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: HttpUrl
    type: str


class ResourceCreate(ResourceBase):
    pass


class ResourceRead(ResourceBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[HttpUrl] = None
    type: Optional[str] = None
