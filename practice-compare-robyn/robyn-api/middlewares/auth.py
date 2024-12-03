from robyn import Request, status_codes, logger
from robyn.authentication import BearerGetter
from robyn.authentication import AuthenticationHandler, Identity

from schema.response import base_response
from utils.hash_handler import decode_access_token


class BasicAuthHandler(AuthenticationHandler):
    @property
    def unauthorized_response(self):
        return base_response("Unauthorized", status_code=status_codes.HTTP_401_UNAUTHORIZED, success=False)

    def authenticate(self, request: Request):
        token = self.token_getter.get_token(request)

        try:
            payload = decode_access_token(token)
        except Exception as e:
            logger.error(f"Error decoding token: {e}")
            return

        return Identity(claims={"user_id": payload["id"], "username": payload["username"]})


def get_auth_handler() -> BasicAuthHandler:
    return BasicAuthHandler(token_getter=BearerGetter())
