from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from schema.response import base_response
from schema.user import AuthPayload
from logic.message import get_history as db_get_history
from utils.dependencies import get_authorization

router = APIRouter()


@router.get("")
async def list_history(
    auth_payload: AuthPayload | None = Depends(get_authorization),
    session: AsyncSession = Depends(get_session),
):
    if auth_payload is None:
        return base_response("Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)

    histories, error = await db_get_history(session, auth_payload.id)
    if error:
        return base_response(str(error), status_code=status.HTTP_400_BAD_REQUEST, success=False)

    return base_response(
        "Get history success",
        status_code=status.HTTP_200_OK,
        data=[message.model_dump(by_alias=True) for message in histories],
    )
