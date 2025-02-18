from typing import Optional

from ninja import Schema, ModelSchema

from apps.posts.models import Post


class PostSchema(ModelSchema):
    class Meta:
        model = Post
        fields = ['id', 'author', 'likes', 'title', 'content', 'created_at', 'media_url', 'location', 'privacy_setting',
                  'number_of_shares']


class PostCreateSchema(Schema):
    content: str
    title: str
    media_url: Optional[str] = None
    location: Optional[str] = None
    privacy_setting: str


class PostUpdateSchema(Schema):
    content: Optional[str] = None
    title: Optional[str] = None
    media_url: Optional[str] = None
    location: Optional[str] = None
    privacy_setting: Optional[str] = None


class ErrorSchema(Schema):
    message: str

class NoneSchema(Schema):
    success: bool
