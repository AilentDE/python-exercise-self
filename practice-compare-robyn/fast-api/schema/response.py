from pydantic import BaseModel
from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any


class ResponseBody(BaseModel):
    success: bool
    message: str
    data: Any
    detail: str | None


def base_response(
    message: str,
    status_code: int = status.HTTP_200_OK,
    success: bool = True,
    data: Any = None,
    detail: str | None = None,
):
    return JSONResponse(
        status_code=status_code,
        content=ResponseBody(success=success, message=message, data=data, detail=detail).model_dump(),
    )
