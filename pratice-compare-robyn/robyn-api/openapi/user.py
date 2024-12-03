from robyn.types import Body


class LoginUserBody(Body):
    username: str
    password: str


class CreateUserBody(LoginUserBody):
    email: str
