from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
