from fastapi import APIRouter, Depends, status, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from schema.response import base_response
from schema.user import AuthPayload
from logic.subscribe import subscribe_user, unsubscribe_user
from utils.dependencies import get_authorization

router = APIRouter()


@router.post("/{user_id}/join")
async def subscribe(
    user_id: str = Annotated[str, Path()],
    auth_payload: AuthPayload | None = Depends(get_authorization),
    session: AsyncSession = Depends(get_session),
):
    if auth_payload is None:
        return base_response("Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)

    _, error = await subscribe_user(session, auth_payload.id, user_id)
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Subscribe success", status_code=status.HTTP_200_OK, data={"target": user_id})


@router.post("/{user_id}/withdraw")
async def unsubscribe(
    user_id: str = Annotated[str, Path()],
    auth_payload: AuthPayload | None = Depends(get_authorization),
    session: AsyncSession = Depends(get_session),
):
    if auth_payload is None:
        return base_response("Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)

    _, error = await unsubscribe_user(session, auth_payload.id, user_id)
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Unsubscribed", status_code=status.HTTP_200_OK, data={"target": user_id})
