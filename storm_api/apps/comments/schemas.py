from ninja import ModelSchema, Schema

from .models import Comment
from ..users.schemas import UserSchema


class CommentSchema(ModelSchema):
    user: UserSchema
    likes: list[UserSchema]
    reportes: list[UserSchema]
    
    class Config:
        model = Comment
        model_fields = "__all__"


class CommentCreateSchema(Schema):
    content: str


class CommentUpdateSchema(Schema):
    content: str


class ErrorSchema(Schema):
    message: str
