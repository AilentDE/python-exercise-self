from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.user import User
from schemas.user import UserCreate
from config.db_postgres import get_async_session
from routes.users_fake import router as fake_router

router = APIRouter()
router.include_router(fake_router, prefix="/fake")


@router.get("/")
async def get_all_users(
    db: AsyncSession = Depends(get_async_session), skip: Annotated[int, Query] = 0, limit: Annotated[int, Query] = 10
):
    stmt = select(User).offset(skip).limit(limit)

    try:
        result = await db.execute(stmt)
        users = result.scalars().all()
        return {'message': 'query success', 'data': jsonable_encoder(users)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        await db.rollback()


@router.post("/")
async def create_user(user: Annotated[UserCreate, Body], db: AsyncSession = Depends(get_async_session)):
    stmt = insert(User).values(**user.model_dump())
    try:
        await db.execute(stmt)
        await db.commit()
        return {"message": "User created successfully"}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="existing user")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        await db.rollback()


@router.delete('/')
async def clear_all_users(db: AsyncSession = Depends(get_async_session)):
    try:
        await db.execute(delete(User))
        await db.commit()
        return {"message": "All users deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        await db.rollback()
