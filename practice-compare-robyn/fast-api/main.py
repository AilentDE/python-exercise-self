from loguru import logger
from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes.user import router as user_router
from routes.subscribe import router as subscribe_router
from routes.message import router as message_router
from routes.history import router as history_router

from config.database import create_all
from utils.db_base import create_base_premission


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all()
    await create_base_premission()
    yield
    logger.info("Shutting down")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix='/auth', tags=["User"])
app.include_router(subscribe_router, prefix='/subscribe', tags=["Subscribe"])
app.include_router(message_router, prefix='/message', tags=["Message"])
app.include_router(history_router, prefix='/history', tags=["History"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
