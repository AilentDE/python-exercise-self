from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schema.user import UserRegister, UserLogin, AuthPayload
from utils.hash_handler import create_access_token


async def creater_user(session: AsyncSession, user: UserRegister) -> tuple[str | None, Exception | None]:
    try:
        new_user = User(**user.model_dump())
        new_user.hash_password()

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        access_token = create_access_token(AuthPayload(id=str(new_user.id), username=new_user.username))
        return (access_token, None)
    except IntegrityError:
        return (None, Exception("Username or email already exists"))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return (None, Exception("Error occurred while creating user"))


async def login_user(session: AsyncSession, user: UserLogin) -> tuple[str | None, Exception | None]:
    try:
        stmt = select(User).where(User.username == user.username)
        result = await session.execute(stmt)
        found_user = result.scalar_one_or_none()
        if found_user is None:
            return (None, Exception("User not found"))

        if not found_user.check_password(user.password):
            return (None, Exception("Password error"))
        else:
            access_token = create_access_token(AuthPayload(id=str(found_user.id), username=found_user.username))
            return (access_token, None)
    except Exception as e:
        logger.error(f"Error finding user: {e}")
        return (None, Exception("Error occurred while finding user"))
