from fastapi import Header
from typing import Annotated

from utils.hash_handler import decode_access_token


async def get_authorization(authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        return None
    access_token = authorization.split("Bearer ")[1]
    return decode_access_token(access_token)
