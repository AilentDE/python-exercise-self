from bcrypt import hashpw, checkpw
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os


HASH_SECRET = os.getenv('ROBYN_HASH_SALT')
ALGORITHM = os.getenv('ROBYN_ALGORITHM')
SECRETE_KEY = os.getenv('ROBYN_SECRET_KEY')


def get_password_hash(password: str) -> str:
    return hashpw(password.encode(), HASH_SECRET.encode()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, HASH_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, str]:
    try:
        return jwt.decode(token, HASH_SECRET, algorithms=[ALGORITHM])
    except JWTError as e:
        raise e
    except Exception:
        raise Exception("Error decoding token")
