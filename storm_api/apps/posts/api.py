from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Form, Router
from ninja.responses import Response

from common.auth import AuthBearer
from .models import Post
from .schemas import (
    ErrorSchema,
    NoneSchema,
    PostCreateSchema,
    PostSchema,
    PostUpdateSchema,
)
from .services import PostService

router = Router(tags=["posts"])


@router.get("/", response={200: list[PostSchema], 403: ErrorSchema}, auth=AuthBearer())
def list_posts(request: HttpRequest) -> QuerySet[Post] | Response:
    try:
        return PostService.get_posts()
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.get(
    "/{post_id}", response={200: PostSchema, 403: ErrorSchema}, auth=AuthBearer()
)
def get_post(request: HttpRequest, post_id: int) -> Post | Response:
    try:
        return PostService.get_post(post_id=post_id)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.post(
    "/create",
    response={200: PostSchema, 201: PostSchema, 403: ErrorSchema},
    auth=AuthBearer(),
)
def create_post(request: HttpRequest, data: Form[PostCreateSchema]) -> Post | Response:
    try:
        return PostService.create_posts(request=request, data=data)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.patch(
    "/{post_id}", response={200: PostSchema, 403: ErrorSchema}, auth=AuthBearer()
)
def update_post(request: HttpRequest, post_id: int, data: PostUpdateSchema) -> Post | Response:
    try:
        return PostService.update_post(post_id=post_id, payload=data)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.delete(
    "/{post_id}", response={200: NoneSchema, 403: ErrorSchema}, auth=AuthBearer()
)
def delete_post(request: HttpRequest, post_id: int) -> dict[str, bool] | Response:
    try:
        PostService.delete_post(post_id=post_id)
        return {"success": True}
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.post("/{post_id}/like", response={
    200: NoneSchema,
    403: ErrorSchema,
    404: ErrorSchema
}, auth=AuthBearer())
def like_post(request: HttpRequest, post_id: int):
    try:
        PostService.like_posts(request=request, post_id=post_id)
        return Response({"success": True}, status=200)
    except Exception as error:
        return Response({"error": str(error)}, status=500)
