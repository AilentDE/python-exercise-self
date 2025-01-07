from fastapi import APIRouter

from config.custom_logger import logger
from schema.log import LogSchema

router = APIRouter()


@router.post("/log")
async def log(log: LogSchema):
    logger.info(log.message)
    return {"message": "Logged", "data": log.model_dump()}
