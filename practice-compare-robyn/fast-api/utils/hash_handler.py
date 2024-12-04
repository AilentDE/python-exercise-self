from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
import jwt
import os

from schema.user import AuthPayload


ALGORITHM = os.getenv('ALGORITHM')
SECRETE_KEY = os.getenv('SECRET_KEY')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: AuthPayload, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.model_dump()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> AuthPayload:
    try:
        return AuthPayload(**jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM]))
    except InvalidTokenError as e:
        raise e
    except Exception:
        raise Exception("Error decoding token")
