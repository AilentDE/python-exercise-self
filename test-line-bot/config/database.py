from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config.setting import DatabaseSetting

engine = create_async_engine(f"sqlite+aiosqlite:///{DatabaseSetting.host}", echo=True)
async_sessionmaker = async_sessionmaker(engine)

Base = declarative_base()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_sessionmaker() as session:
        yield session


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
