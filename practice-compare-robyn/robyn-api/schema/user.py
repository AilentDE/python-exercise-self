from dataclasses import dataclass


@dataclass(slots=False)
class UserLogin:
    username: str
    password: str


@dataclass(slots=False)
class UserRegister(UserLogin):
    email: str


@dataclass(slots=False)
class UserOutput:
    id: str
    username: str
    email: str
