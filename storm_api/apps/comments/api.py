from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router, Schema
from ninja.pagination import PageNumberPagination, paginate
from ninja.responses import Response

from apps.comments.models import Comment
from common.auth import AuthBearer
from .schemas import CommentCreateSchema, CommentSchema, CommentUpdateSchema, ErrorSchema
from .services import CommentsServices

router = Router(tags=["comments"])


class NoneSchema(Schema):
    success: bool


@router.get("/", response={200: list[CommentSchema], 403: ErrorSchema}, auth=AuthBearer())
@paginate(PageNumberPagination, page_size=100)
def comments_list(request: HttpRequest) -> Response | QuerySet[Comment]:
    try:
        return CommentsServices.get_comments()
    except Exception as error:
        return Response({"message": str(error)}, status=500)


@router.get("/post/{post_id}", response={200: list[CommentSchema], 403: ErrorSchema}, auth=AuthBearer())
def comment_of_post(request: HttpRequest, post_id: int) -> Response | QuerySet[Comment]:
    try:
        return CommentsServices.get_comments_by_post(post_id=post_id)
    except Exception as error:
        return Response({"message": str(error)}, status=500)


@router.get("/user/{user_id}", response={200: list[CommentSchema], 403: ErrorSchema}, auth=AuthBearer())
def comment_of_user(request: HttpRequest, user_id: int) -> Response | QuerySet[Comment]:
    try:
        return CommentsServices.get_comments_by_user(user_id=user_id)
    except Exception as error:
        return Response({"message": str(error)}, status=500)


@router.get("/username/{username}", response={200: list[CommentSchema], 403: ErrorSchema}, auth=AuthBearer())
def comment_of_username(request: HttpRequest, username: str) -> Response | QuerySet[Comment]:
    try:
        return CommentsServices.get_comments_by_username(username=username)
    except Exception as error:
        return Response({"message": str(error)}, status=500)


@router.get("/post/{post_id}/status/{status}", response={200: list[CommentSchema], 403: ErrorSchema}, auth=AuthBearer())
def comment_by_status(request: HttpRequest, post_id: int, status: str) -> Response | QuerySet[Comment]:
    try:
        return CommentsServices.get_comments_by_status(status=status, post_id=post_id)
    except Exception as error:
        return Response({"message": str(error)}, status=500)


@router.post("/create/{post_id}", response={200: CommentSchema, 201: CommentSchema, 403: ErrorSchema},
             auth=AuthBearer())
def create_comment(request: HttpRequest, post_id: int, payload: CommentCreateSchema) -> Response | Comment:
    try:
        return CommentsServices.create_comment(request=request, payload=payload, post_id=post_id)
    except Exception as error:
        return Response({"message": str(error)}, status=500)


@router.patch("/update/{comment_id}", response={200: CommentSchema, 403: ErrorSchema}, auth=AuthBearer())
def update_comment(request: HttpRequest, comment_id: int, payload: CommentUpdateSchema):
    try:
        return CommentsServices.update_comment(comment_id=comment_id, payload=payload)
    except Exception as error:
        return Response({"message": str(error)}, status=500)


@router.post("/{comment_id}/like", response={
    200: NoneSchema,
    403: ErrorSchema,
    404: ErrorSchema
}, auth=AuthBearer())
def like_post(request: HttpRequest, comment_id: int) -> Response:
    try:
        CommentsServices.like_comment(request=request, comment_id=comment_id)
        return Response({"success": True}, status=200)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.delete("/{comment_id}", response={200: NoneSchema, 403: ErrorSchema}, auth=AuthBearer())
def delete_comment(request: HttpRequest, comment_id: int) -> Response:
    try:
        CommentsServices.desactivate_comment(comment_id=comment_id)
        return Response({"success": True}, status=200)
    except Exception as error:
        return Response({"message": str(error)}, status=500)
