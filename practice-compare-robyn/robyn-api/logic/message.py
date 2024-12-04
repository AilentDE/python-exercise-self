from robyn import logger
from sqlalchemy import select, delete, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from dataclasses import asdict
from uuid import UUID

from models.time_mixin import utc_now
from models.user import User, UserSubscriptions
from models.message import Message, ReadHistory
from schema.user import UserOutput
from schema.message import MessageCreate, MessageOutputCreated, MessageOutputList, MessageOutputFull
from utils.time_handler import formated_datetime


async def create_message(
    session: AsyncSession, message: MessageCreate
) -> tuple[MessageOutputCreated | None, Exception | None]:
    try:
        new_message = Message(**asdict(message))

        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)

        return (
            MessageOutputCreated(
                id=str(new_message.id),
                authorId=str(new_message.author_id),
                title=new_message.title,
                content=new_message.content,
                permissionLevel=new_message.permission_level,
                createdAt=formated_datetime(new_message.created_at),
                updatedAt=formated_datetime(new_message.updated_at),
            ),
            None,
        )
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        return (None, Exception("Error occurred while creating message"))


async def get_messages(
    session: AsyncSession, user_id: str = "", skip: int = 0, limit: int = 10
) -> tuple[list[MessageOutputList], Exception | None]:

    search_permission = (0, 1)

    try:
        stmt = select(Message, User).join(User).offset(skip).limit(limit).order_by(Message.created_at.desc())
        if user_id:
            stmt = stmt.where(or_(Message.permission_level.in_(search_permission), Message.author_id == user_id))
        else:
            stmt = stmt.where(Message.permission_level.in_(search_permission))
        result = await session.execute(stmt)
        messages = result.all()
        return (
            [
                MessageOutputList(
                    id=str(message.id),
                    author=UserOutput(
                        id=str(user.id),
                        username=user.username,
                        email=user.email,
                    ),
                    title=message.title,
                    createdAt=formated_datetime(message.created_at),
                    updatedAt=formated_datetime(message.updated_at),
                )
                for message, user in messages
            ],
            None,
        )
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        return ([], Exception("Error occurred while getting messages"))


async def insert_record(session: AsyncSession, user_id: str, message_id: str) -> tuple[bool, Exception | None]:
    try:
        stmt_record = (
            insert(ReadHistory)
            .values(user_id=UUID(user_id), message_id=UUID(message_id))
            .on_conflict_do_update(index_elements=["user_id", "message_id"], set_={"updated_at": utc_now()})
        )
        await session.execute(stmt_record)
        await session.commit()
        return (True, None)
    except Exception as e:
        logger.error(f"Error inserting record: {e}")
        return (False, Exception("Error occurred while inserting record"))


async def get_message(
    session: AsyncSession, message_id: str, user_id: str = ""
) -> tuple[MessageOutputFull | None, Exception | None]:
    try:
        if not user_id:
            stmt = select(Message, User).join(User).where(Message.id == UUID(message_id), Message.permission_level == 0)
        else:
            stmt = (
                select(Message, User, UserSubscriptions)
                .join(User, User.id == Message.author_id)
                .outerjoin(
                    UserSubscriptions,
                    and_(UserSubscriptions.user_id == UUID(user_id), UserSubscriptions.author_id == Message.author_id),
                )
                .where(Message.id == UUID(message_id))
            )
        result = await session.execute(stmt)
        if message_result := result.first():
            if not user_id:
                message, user = message_result
                subscription = None
            else:
                message, user, subscription = message_result
                session.expunge_all()
                _, error = await insert_record(session, user_id, message_id)
                if error:
                    return (None, error)
        else:
            return (None, Exception("Message not found"))

        if str(message.author_id) == user_id:
            pass
        elif message.permission_level == 2 or (message.permission_level == 1 and subscription is None):
            return (None, Exception("Permission denied"))

        return (
            MessageOutputFull(
                id=str(message.id),
                author=UserOutput(
                    id=str(user.id),
                    username=user.username,
                    email=user.email,
                ),
                title=message.title,
                content=message.content,
                permissionLevel=message.permission_level,
                createdAt=formated_datetime(message.created_at),
                updatedAt=formated_datetime(message.updated_at),
            ),
            None,
        )
    except Exception as e:
        logger.error(f"Error getting message: {e}")
        return (None, Exception("Error occurred while getting message"))


async def delete_message(session: AsyncSession, message_id: str, user_id: str) -> tuple[bool, Exception | None]:
    try:
        stmt = delete(Message).where(Message.id == UUID(message_id), Message.author_id == UUID(user_id))
        await session.execute(stmt)
        await session.commit()
        return (True, None)
    except Exception as e:
        logger.error(f"Error deleting message: {e}")
        return (False, Exception("Error occurred while deleting message"))


async def get_history(
    session: AsyncSession, user_id: str, skip: int = 0, limit: int = 10
) -> tuple[list[MessageOutputList], Exception | None]:
    try:
        stmt = (
            select(ReadHistory, Message, User)
            .join(Message, ReadHistory.message_id == Message.id)
            .join(User, Message.author_id == User.id)
            .offset(skip)
            .limit(limit)
            .where(ReadHistory.user_id == UUID(user_id))
            .order_by(ReadHistory.updated_at.desc())
        )
        result = await session.execute(stmt)
        messages = result.all()
        return (
            [
                MessageOutputList(
                    id=str(message.id),
                    author=UserOutput(
                        id=str(user.id),
                        username=user.username,
                        email=user.email,
                    ),
                    title=message.title,
                    createdAt=formated_datetime(message.created_at),
                    updatedAt=formated_datetime(message.updated_at),
                )
                for _, message, user in messages
            ],
            None,
        )
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return ([], Exception("Error occurred while getting history"))
