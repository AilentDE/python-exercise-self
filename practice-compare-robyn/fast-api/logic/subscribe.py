from loguru import logger
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models.time_mixin import utc_now
from models.user import UserSubscriptions


async def subscribe_user(session: AsyncSession, user_id: str, target_id: str) -> tuple[bool, Exception | None]:
    try:
        stmt = (
            insert(UserSubscriptions)
            .values(user_id=user_id, author_id=target_id)
            .on_conflict_do_update(index_elements=["user_id", "author_id"], set_={"updated_at": utc_now()})
        )
        await session.execute(stmt)
        await session.commit()
        return (True, None)
    except Exception as e:
        logger.error(f"Error subscribing user: {e}")
        return (False, Exception("Error occurred while subscribing user"))


async def unsubscribe_user(session: AsyncSession, user_id: str, target_id: str) -> tuple[bool, Exception | None]:
    try:
        stmt = delete(UserSubscriptions).where(
            UserSubscriptions.user_id == user_id, UserSubscriptions.author_id == target_id
        )
        await session.execute(stmt)
        await session.commit()
        return (True, None)
    except Exception as e:
        logger.error(f"Error unsubscribing user: {e}")
        return (False, Exception("Error occurred while unsubscribing user"))
