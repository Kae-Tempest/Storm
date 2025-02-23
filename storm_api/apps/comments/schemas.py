from ninja import ModelSchema, Schema

from ..users.schemas import UserSchema
from .models import Comment


class CommentSchema(ModelSchema):
    user: UserSchema
    likes: list[UserSchema]
    reportes: list[UserSchema]

    class Config:
        model = Comment
        model_fields = "__all__"


class CommentCreateSchema(Schema):
    content: str
    parent_comment: int | None = None


class CommentUpdateSchema(Schema):
    content: str


class ErrorSchema(Schema):
    message: str
