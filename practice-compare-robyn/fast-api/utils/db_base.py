from loguru import logger

from config.database import get_session
from models.message import MessagePremission


async def create_base_premission():
    async for session in get_session():
        session.add_all(MessagePremission.base_premission())
        await session.commit()
        logger.info("Base premission created")
