from robyn import SubRouter, Request, status_codes

from middlewares.auth import get_auth_handler
from config.database import get_session
from schema.response import base_response
from logic.message import get_history as db_get_history

router = SubRouter(__name__, prefix="/history")
router.configure_authentication(get_auth_handler())


@router.get("", auth_required=True)
async def list_history(request: Request):
    async for session in get_session():
        history, error = await db_get_history(session, request.identity.claims["user_id"])
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Get history success", status_code=status_codes.HTTP_200_OK, data=history)
