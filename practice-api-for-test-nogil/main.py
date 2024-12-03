from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger

from middlewares.timer import TimerMiddleware
from config.db_postgres import init_db
from routes.users import router as users_router
from utils.system_check import check_gil


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup")
    await init_db()
    check_gil()
    yield
    logger.info("Shutdown")


app = FastAPI(lifespan=lifespan)
app.add_middleware(TimerMiddleware)
app.include_router(users_router, prefix="/api/users")
