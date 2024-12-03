from robyn import SubRouter, Request, status_codes

from middlewares.auth import get_auth_handler
from config.database import get_session
from schema.response import base_response
from schema.message import MessageCreate
from logic.message import (
    create_message as db_create_message,
    get_messages as db_get_messages,
    get_message as db_get_message,
    delete_message as db_delete_message,
)

router = SubRouter(__name__, prefix="/message")
router.configure_authentication(get_auth_handler())


@router.get("s/")
async def list_messages(request: Request):
    async for session in get_session():
        messages, error = await db_get_messages(session)
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Get messages success", status_code=status_codes.HTTP_200_OK, data=messages)


@router.get("s/auth", auth_required=True)
async def list_messages_with_auth(request: Request):
    async for session in get_session():
        messages, error = await db_get_messages(session, request.identity.claims["user_id"])
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Get messages with auth success", status_code=status_codes.HTTP_200_OK, data=messages)


@router.get("/:message_id")
async def get_message(request: Request):
    message_id = request.path_params.get("message_id")
    if not message_id:
        return base_response("Invalid message id", status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    async for session in get_session():
        message, error = await db_get_message(session, message_id)
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Get message success", status_code=status_codes.HTTP_200_OK, data=message)


@router.get("/:message_id/auth", auth_required=True)
async def get_message_with_auth(request: Request):
    message_id = request.path_params.get("message_id")
    if not message_id:
        return base_response("Invalid message id", status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    async for session in get_session():
        message, error = await db_get_message(session, message_id, request.identity.claims["user_id"])
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Get message with auth success", status_code=status_codes.HTTP_200_OK, data=message)


@router.post("/create", auth_required=True)
async def create_message(request: Request):
    try:
        input_body = request.json()
        message_schema = MessageCreate(
            author_id=request.identity.claims["user_id"],
            title=input_body["title"],
            content=input_body["content"],
            permission_level=int(input_body["permission_level"]),
        )
    except Exception:
        return base_response(
            "Invalid request body", status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY, success=False
        )

    async for session in get_session():
        message_output, error = await db_create_message(session, message_schema)
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    return base_response(
        "Create message success", status_code=status_codes.HTTP_201_CREATED, data={"message": message_output}
    )


@router.delete("/:message_id/delete", auth_required=True)
async def delete_message(request: Request):
    message_id = request.path_params.get("message_id")
    if not message_id:
        return base_response("Invalid message id", status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    async for session in get_session():
        _, error = await db_delete_message(session, message_id, request.identity.claims["user_id"])
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

    return base_response("Delete message success", status_code=status_codes.HTTP_200_OK, data={"messageId": message_id})
