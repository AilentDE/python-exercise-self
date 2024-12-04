from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    email: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(UserLogin):
    email: str


class AuthPayload(BaseModel):
    id: str
    username: str
