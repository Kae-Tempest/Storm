from ninja import Schema

from apps.users.schemas import UserSchema


class LoginSchema(Schema):
    email: str
    password: str


class RegisterSchema(Schema):
    username: str
    password: str
    email: str
    display_name: str


class TokenSchema(Schema):
    access_token: str
    token_type: str = "bearer"


class RegisterTokenSchema(TokenSchema):
    user: UserSchema


class ErrorSchema(Schema):
    detail: str
