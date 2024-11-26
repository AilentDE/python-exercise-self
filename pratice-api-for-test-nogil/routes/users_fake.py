from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from threading import Thread
from loguru import logger
from faker import Faker
from uuid import uuid4
import asyncio
import time

from config.db_redis import get_redis
from config.db_postgres import get_async_session
from models.user import User
from schemas.user import UserCreate
from utils.create_fake_user import create_fake_user, create_fake_user_independent

faker = Faker()
router = APIRouter()


@router.post("/")
async def create_fake_users(db: AsyncSession = Depends(get_async_session), count: Annotated[int, Query] = 10):
    start = time.time()
    success_counts = defaultdict(int)

    for _ in range(count):
        user = UserCreate(
            username=faker.user_name(), email=faker.email(), password=faker.password(), full_name=faker.name()
        )
        try:
            stmt = insert(User).values(**user.model_dump())
            await db.execute(stmt)
            await db.commit()
            success_counts["success"] += 1
        except Exception:
            success_counts["fail"] += 1
            # print(e)
        finally:
            await db.rollback()

    cost_time = f"{(time.time() - start) * 1000:.2f} ms"
    logger.success(f"create {count} fake users cost {cost_time}")
    return {"message": f"you have {success_counts['success']} success and {success_counts['fail']} fail"}


@router.post("/background")
async def create_fake_users_background(
    rd: Redis = Depends(get_redis),
    count: Annotated[int, Query] = 10,
):
    start = time.time()
    task_id = str(uuid4())
    stream_key = f"{task_id}_stream"

    success_counts = defaultdict(int)

    for _ in range(count):
        user = UserCreate(
            username=faker.user_name(), email=faker.email(), password=faker.password(), full_name=faker.name()
        )
        # [IMPORTANT] can't use background task since async function
        asyncio.create_task(create_fake_user(user, count, task_id, rd, success_counts))

    await rd.xread({stream_key: 0}, count=1, block=30 * 1000)
    await rd.delete(stream_key)
    cost_time = f"{(time.time() - start) * 1000:.2f} ms"
    logger.success(f"create {count} fake users cost {cost_time}")
    return {"message": f"you have {success_counts['success']} success and {success_counts['fail']} fail"}


@router.post("/thread")
async def create_fake_users_thread(
    rd: Redis = Depends(get_redis),
    count: Annotated[int, Query] = 10,
):
    start = time.time()
    task_id = str(uuid4())
    counter_key = f"{task_id}_count"
    success_key = f"{task_id}_success"

    await rd.set(counter_key, 0, 3600)
    await rd.set(success_key, 0, 3600)
    threads = []
    for _ in range(count):
        user = UserCreate(
            username=faker.user_name(), email=faker.email(), password=faker.password(), full_name=faker.name()
        )
        thread = Thread(target=create_fake_user_independent, args=(user, task_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    cost_time = f"{(time.time() - start) * 1000:.2f} ms"
    logger.success(f"create {count} fake users cost {cost_time}")
    final_success = int(await rd.get(success_key))
    return {"message": f"you have {final_success} success and {count - final_success} fail"}


@router.post("/process")
async def create_fake_users_process(
    rd: Redis = Depends(get_redis),
    count: Annotated[int, Query] = 10,
):
    start = time.time()
    task_id = str(uuid4())
    counter_key = f"{task_id}_count"
    success_key = f"{task_id}_success"

    await rd.set(counter_key, 0, 3600)
    await rd.set(success_key, 0, 3600)

    cpus = cpu_count()
    with Pool(cpus) as pool:
        users = [
            UserCreate(
                username=faker.user_name(), email=faker.email(), password=faker.password(), full_name=faker.name()
            )
            for _ in range(count)
        ]
        pool.starmap(create_fake_user_independent, [(user, task_id) for user in users])

        cost_time = f"{(time.time() - start) * 1000:.2f} ms"
        logger.success(f"create {count} fake users cost {cost_time}")
        final_success = int(await rd.get(success_key))
        return {"message": f"you have {final_success} success and {count - final_success} fail"}
