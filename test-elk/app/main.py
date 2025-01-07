from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.custom_logger import logger

from router.log import router as log_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    yield
    logger.info("Shutting down application")


app = FastAPI(lifespan=lifespan)
app.include_router(log_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
