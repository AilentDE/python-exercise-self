from fastapi import APIRouter, Depends, Body, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from schema.user import UserRegister, UserLogin
from schema.response import base_response
from logic.user import creater_user, login_user

router = APIRouter()


@router.post("/register")
async def register(user: Annotated[UserRegister, Body()], session: AsyncSession = Depends(get_session)):
    access_token, error = await creater_user(session, user)
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response(
        "User created successfully", status_code=status.HTTP_201_CREATED, data={"accessToken": access_token}
    )


@router.post("/login")
async def login(user: Annotated[UserLogin, Body()], session: AsyncSession = Depends(get_session)):
    access_token, error = await login_user(session, user)
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response(
        "User logged in successfully", status_code=status.HTTP_200_OK, data={"accessToken": access_token}
    )
