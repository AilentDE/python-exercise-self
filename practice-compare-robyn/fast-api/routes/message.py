from fastapi import APIRouter, status, Depends, Body, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from schema.response import base_response
from schema.user import AuthPayload
from schema.message import MessageCreate
from logic.message import (
    create_message as db_create_message,
    delete_message as db_delete_message,
    get_messages as db_get_messages,
    get_message as db_get_message,
)
from utils.dependencies import get_authorization

router = APIRouter()


@router.get("s")
@router.get("s/auth")
async def list_messages(
    auth_payload: AuthPayload | None = Depends(get_authorization),
    session: AsyncSession = Depends(get_session),
):
    messages, error = await db_get_messages(session, auth_payload.id if auth_payload else "")
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response(
        f"Get messages {"with auth " if auth_payload else ""}success",
        status_code=status.HTTP_200_OK,
        data=[message.model_dump(by_alias=True) for message in messages],
    )


@router.get("/{message_id}")
@router.get("/{message_id}/auth")
async def get_message(
    message_id: Annotated[str, Path()],
    auth_payload: AuthPayload | None = Depends(get_authorization),
    session: AsyncSession = Depends(get_session),
):
    message, error = await db_get_message(session, message_id, auth_payload.id if auth_payload else "")
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response(
        f"Get message {"with auth " if auth_payload else ""}success",
        status_code=status.HTTP_200_OK,
        data=message.model_dump(by_alias=True),
    )


@router.post("/create")
async def create_message(
    message: Annotated[MessageCreate, Body()],
    auth_payload: AuthPayload | None = Depends(get_authorization),
    session: AsyncSession = Depends(get_session),
):
    if auth_payload is None:
        return base_response("Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)

    created_message, error = await db_create_message(session, auth_payload.id, message)
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response(
        "Create message success", status_code=status.HTTP_201_CREATED, data=created_message.model_dump(by_alias=True)
    )


@router.delete("/{message_id}/delete")
async def delete_message(
    message_id: Annotated[str, Path()],
    auth_payload: AuthPayload | None = Depends(get_authorization),
    session: AsyncSession = Depends(get_session),
):
    if auth_payload is None:
        return base_response("Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)

    _, error = await db_delete_message(session, auth_payload.id, message_id)
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Delete message success", status_code=status.HTTP_200_OK, data={"messageId": message_id})
