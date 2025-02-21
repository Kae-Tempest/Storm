from typing import Optional

from apps.posts.models import Post
from ninja import ModelSchema, Schema


class PostSchema(ModelSchema):
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "likes",
            "title",
            "content",
            "created_at",
            "media_url",
            "location",
            "privacy_setting",
            "number_of_shares",
        ]


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
