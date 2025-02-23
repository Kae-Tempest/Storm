from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja.responses import Response

from apps.comments.models import Comment, StatusChoices
from apps.comments.schemas import CommentCreateSchema, CommentUpdateSchema
from apps.users.models import CustomUser


class CommentsServices:
    @staticmethod
    def get_comments() -> QuerySet[Comment]:
        return Comment.objects.all()

    @staticmethod
    def get_comments_by_post(post_id: int) -> QuerySet[Comment]:
        return Comment.objects.filter(post_id=post_id)

    @staticmethod
    def get_comments_by_user(user_id: int) -> QuerySet[Comment]:
        return Comment.objects.filter(user_id=user_id)

    @staticmethod
    def get_comments_by_username(username: str) -> QuerySet[Comment]:
        user = get_object_or_404(CustomUser, username=username)
        return Comment.objects.filter(user_id=user.id)

    @staticmethod
    def get_comments_by_status(status: str, post_id: int) -> QuerySet[Comment]:
        return Comment.objects.filter(status=status, post_id=post_id)

    @staticmethod
    def create_comment(request: HttpRequest, payload: CommentCreateSchema, post_id: int) -> Comment | Response:
        user = cast(CustomUser, request.user)
        if payload.parent_comment is not None:
            parent = get_object_or_404(Comment, id=payload.parent_comment)
            comment = Comment.objects.create(user=user, post_id=post_id, parent_comment=parent, content=payload.content)
            return comment
        else:
            comment = Comment.objects.create(user=user, post_id=post_id, content=payload.content)
            return comment

    @staticmethod
    def update_comment(comment_id: int, payload: CommentUpdateSchema) -> Comment:
        comment = get_object_or_404(Comment, id=comment_id)

        data = payload.dict(exclude_unset=True)
        for attr, value in data.items():
            setattr(comment, attr, value)

        comment.save()
        return comment

    @staticmethod
    def like_comment(request: HttpRequest, comment_id: int) -> None:
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

    @staticmethod
    def desactivate_comment(comment_id: int) -> None:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.status = StatusChoices.DELETED
        comment.save()
