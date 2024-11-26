from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(os.getenv("DB_URL"))
async_session = async_sessionmaker(engine)

Base = declarative_base()


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        return session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized")
