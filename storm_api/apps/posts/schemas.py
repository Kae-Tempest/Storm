from datetime import datetime
from typing import Optional

from ninja import ModelSchema, Schema, UploadedFile, Form

from apps.posts.models import Post
from apps.users.schemas import UserSchema


class PostSchema(ModelSchema):
    likes: list[UserSchema]
    author: UserSchema

    class Meta:
        model = Post
        fields = "__all__"


class PostOutSchema(Schema):
    id: int
    content: str
    media_url: Optional[str] = None
    location: Optional[str] = None
    privacy_setting: str
    created_at: datetime
    number_of_shares: int
    author: UserSchema
    likes_count: int
    comments_count: int
    is_liked: bool


class PostCreateSchema(Schema):
    content: str = Form(...),
    privacy_setting: str = Form(...),
    media_url: UploadedFile | None = None
    location: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class PostUpdateSchema(Schema):
    content: str | None = None
    media_url: str | None = None
    location: str | None = None
    privacy_setting: str | None = None


class ErrorSchema(Schema):
    message: str


class NoneSchema(Schema):
    success: bool
