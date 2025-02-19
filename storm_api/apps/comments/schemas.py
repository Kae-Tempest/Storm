from ninja import Schema, ModelSchema
from .models import Comment


class CommentSchema(ModelSchema):
    class Config:
        model = Comment
        model_fields = "__all__"


class CommentCreateSchema(Schema):
    content: str


class ErrorSchema(Schema):
    message: str
