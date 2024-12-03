from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from redis.asyncio import Redis as async_redis
from redis import Redis as base_redis
from loguru import logger
import os

from models.user import User
from schemas.user import UserCreate
from config.db_postgres import async_session

DB_URL = os.getenv("DB_URL2")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# 使用 QueuePool 來管理連接池
engine = create_engine(DB_URL, poolclass=QueuePool, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_fake_user(
    user_data: UserCreate, count: int, task_id: str, rd: async_redis, mission_temp: dict[str, int]
):
    stream_key = f"{task_id}_stream"

    user = User(**user_data.model_dump())
    session = async_session()
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        mission_temp["success"] += 1
    except Exception:
        mission_temp["fail"] += 1
    finally:
        await session.close()

        if mission_temp["success"] + mission_temp["fail"] == count:
            await rd.xadd(stream_key, {"task_id": task_id, "count": count})


def create_fake_user_independent(user_data: UserCreate, task_id: str):
    counter_key = f"{task_id}_count"
    success_key = f"{task_id}_success"

    with SessionLocal() as session:
        with base_redis(password=REDIS_PASSWORD) as rd:
            user = User(**user_data.model_dump())
            try:
                session.add(user)
                session.commit()
                rd.incr(success_key)
            except Exception as e:
                logger.error(str(e))
            finally:
                rd.incr(counter_key)
