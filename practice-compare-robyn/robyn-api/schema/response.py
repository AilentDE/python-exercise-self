from typing import Any
from robyn import Response, status_codes, jsonify


def base_response(
    message: str,
    status_code: int = status_codes.HTTP_200_OK,
    success: bool = True,
    data: Any = None,
    detail: str | None = None,
):
    return Response(
        status_code=status_code,
        headers={
            "Content-Type": "application/json",
        },
        description=jsonify({"success": success, "message": message, "data": data, "detail": detail}),
    )
