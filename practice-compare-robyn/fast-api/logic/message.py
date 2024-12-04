from loguru import logger
from sqlalchemy import select, delete, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from uuid import UUID

from models.time_mixin import utc_now

from models.user import User, UserSubscriptions
from models.message import Message, ReadHistory
from schema.user import User as UserSchema
from schema.message import MessageCreate, MessageCreated, MessageWithAuthor, MessageFull
from utils.time_handler import formated_datetime


async def create_message(
    session: AsyncSession, user_id: str, message: MessageCreate
) -> tuple[MessageCreated | None, Exception | None]:
    try:
        new_message = Message(author_id=UUID(user_id), **message.model_dump())

        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)

        return (
            MessageCreated(
                id=str(new_message.id),
                author_id=user_id,
                title=new_message.title,
                content=new_message.content,
                permission_level=new_message.permission_level,
                created_at=formated_datetime(new_message.created_at),
                updated_at=formated_datetime(new_message.updated_at),
            ),
            None,
        )
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        return (None, Exception("Error occurred while creating message"))


async def delete_message(session: AsyncSession, user_id: str, message_id: str) -> tuple[None, Exception | None]:
    try:
        stmt = delete(Message).where(and_(Message.id == UUID(message_id), Message.author_id == UUID(user_id)))
        await session.execute(stmt)
        await session.commit()
        return (True, None)
    except Exception as e:
        logger.error(f"Error deleting message: {e}")
        return (False, Exception("Error occurred while deleting message"))


async def get_messages(
    session: AsyncSession, user_id: str = "", skip: int = 0, limit: int = 10
) -> tuple[list[MessageWithAuthor], Exception | None]:

    search_permission = (0, 1)

    try:
        stmt = select(Message, User).join(User).offset(skip).limit(limit).order_by(Message.created_at.desc())
        if user_id:
            stmt = stmt.where(or_(Message.permission_level.in_(search_permission), Message.author_id == UUID(user_id)))
        else:
            stmt = stmt.where(Message.permission_level.in_(search_permission))
        result = await session.execute(stmt)
        messages = result.all()
        return [
            MessageWithAuthor(
                id=str(message.id),
                title=message.title,
                created_at=formated_datetime(message.created_at),
                updated_at=formated_datetime(message.updated_at),
                author=UserSchema(id=str(user.id), username=user.username, email=user.email),
            )
            for message, user in messages
        ], None
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        return ([], Exception("Error occurred while getting messages"))


async def insert_record(session: AsyncSession, user_id: str, message_id: str) -> tuple[bool, Exception | None]:
    try:
        stmt = (
            insert(ReadHistory)
            .values(user_id=UUID(user_id), message_id=UUID(message_id))
            .on_conflict_do_update(index_elements=["user_id", "message_id"], set_={"updated_at": utc_now()})
        )
        await session.execute(stmt)
        await session.commit()
        return (True, None)
    except Exception as e:
        logger.error(f"Error inserting record: {e}")
        return (False, Exception("Error occurred while inserting record"))


async def get_message(
    session: AsyncSession, message_id: str, user_id: str = ""
) -> tuple[MessageFull, Exception | None]:
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
            MessageFull(
                id=str(message.id),
                author=UserSchema(
                    id=str(user.id),
                    username=user.username,
                    email=user.email,
                ),
                title=message.title,
                content=message.content,
                permission_level=message.permission_level,
                created_at=formated_datetime(message.created_at),
                updated_at=formated_datetime(message.updated_at),
            ),
            None,
        )

    except Exception as e:
        logger.error(f"Error getting message: {e}")
        return (None, Exception("Error occurred while getting message"))


async def get_history(
    session: AsyncSession, user_id: str, skip: int = 0, limit: int = 10
) -> tuple[list[MessageWithAuthor], Exception | None]:
    try:
        stmt = (
            select(ReadHistory, Message, User)
            .join(Message, ReadHistory.message_id == Message.id)
            .join(User, User.id == Message.author_id)
            .offset(skip)
            .limit(limit)
            .where(ReadHistory.user_id == UUID(user_id))
            .order_by(ReadHistory.updated_at.desc())
        )
        result = await session.execute(stmt)
        messages = result.all()
        return [
            MessageWithAuthor(
                id=str(message.id),
                title=message.title,
                author=UserSchema(id=str(user.id), username=user.username, email=user.email),
                created_at=formated_datetime(message.created_at),
                updated_at=formated_datetime(message.updated_at),
            )
            for _, message, user in messages
        ], None
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return ([], Exception("Error occurred while getting history"))
