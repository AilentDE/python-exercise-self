from robyn import SubRouter, Request, status_codes

from middlewares.auth import get_auth_handler
from config.database import get_session
from schema.response import base_response
from logic.subscribe import subscribe_user, unsubscribe_user

router = SubRouter(__name__, prefix='/subscribe')
router.configure_authentication(get_auth_handler())


@router.post("/:user_id/join", auth_required=True)
async def subscribe(request: Request):
    target_id = request.path_params.get("user_id")
    if not target_id:
        return base_response("User ID not provided", status_code=status_codes.HTTP_400_BAD_REQUEST)

    user_id = request.identity.claims["user_id"]
    async for session in get_session():
        _, error = await subscribe_user(session, user_id, target_id)
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

        return base_response("Subscribe success", status_code=status_codes.HTTP_200_OK, data={"target": target_id})


@router.post("/:user_id/withdraw", auth_required=True)
async def unsubscribe(request: Request):
    target_id = request.path_params.get("user_id")
    if not target_id:
        return base_response("User ID not provided", status_code=status_codes.HTTP_400_BAD_REQUEST)

    user_id = request.identity.claims["user_id"]
    async for session in get_session():
        _, error = await unsubscribe_user(session, user_id, target_id)
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

        return base_response("Unsubscribed", status_code=status_codes.HTTP_200_OK, data={"target": target_id})
