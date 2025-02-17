from ninja import Schema
from datetime import datetime

from ..users.schemas import UserSchema

class PostSchema(Schema):
    id: int
    content: str
    created_at: datetime
    likes_count: int
    is_liked: bool
    author: UserSchema

    @classmethod
    def from_orm(cls, post, request_user=None):
        return cls(
            id=post.pk,
            content=post.content,
            created_at=post.created_at,
            likes_count=post.likes_count,
            is_liked=post.is_liked_by(request_user),
            author=UserSchema.from_orm(post.author)
        )

class PostCreateSchema(Schema):
    content: str

class PostUpdateSchema(Schema):
    content: str

class ErrorSchema(Schema):
    message: str