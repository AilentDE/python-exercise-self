from robyn import SubRouter, Request, status_codes

from openapi.user import CreateUserBody, LoginUserBody

from config.database import get_session
from schema.user import UserRegister, UserLogin
from schema.response import base_response
from logic.user import create_user, login_user

router = SubRouter(__name__, prefix='/auth')


@router.post("/register")
async def register(request: Request, body: CreateUserBody):
    try:
        user_schema = UserRegister(**request.json())
    except Exception:
        return base_response(
            "Invalid request body", status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY, success=False
        )

    async for session in get_session():
        access_token, error = await create_user(session, user_schema)
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

        return base_response(
            "User created successfully", status_code=status_codes.HTTP_201_CREATED, data={"accessToken": access_token}
        )


@router.post("/login")
async def login(request: Request, body: LoginUserBody):
    try:
        user_schema = UserLogin(**request.json())
    except Exception:
        return base_response(
            "Invalid request body", status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY, success=False
        )

    async for session in get_session():
        access_token, error = await login_user(session, user_schema)
        if error:
            return base_response(str(error), status_code=status_codes.HTTP_400_BAD_REQUEST, success=False)

        return base_response(
            "User logged in successfully", status_code=status_codes.HTTP_200_OK, data={"accessToken": access_token}
        )
