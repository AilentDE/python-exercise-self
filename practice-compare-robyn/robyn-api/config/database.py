from robyn import logger

from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

engine = create_async_engine(os.getenv('ROBYN_DB_URL'))
async_session_maker = async_sessionmaker(engine)

Base = declarative_base()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.warn("Database tables recreated")
