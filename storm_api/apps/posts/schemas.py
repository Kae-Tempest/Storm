from apps.posts.models import Post
from apps.users.schemas import UserSchema
from ninja import ModelSchema, Schema


class PostSchema(ModelSchema):
    likes: list[UserSchema]
    author: UserSchema

    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSchema(Schema):
    content: str
    title: str
    media_url: str | None = None
    location: str | None = None
    privacy_setting: str


class PostUpdateSchema(Schema):
    content: str | None = None
    title: str | None = None
    media_url: str | None = None
    location: str | None = None
    privacy_setting: str | None = None


class ErrorSchema(Schema):
    message: str


class NoneSchema(Schema):
    success: bool
