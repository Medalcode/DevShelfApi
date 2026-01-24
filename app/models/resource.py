import uuid
import datetime
from datetime import timezone
from sqlalchemy import Column, String, Text, DateTime
from app.models.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(1024), nullable=False)
    type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Resource(id={self.id} title={self.title})>"
