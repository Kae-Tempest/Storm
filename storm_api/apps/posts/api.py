from ninja import Path, Router, Form
from typing import List

from ninja.responses import Response

from common.auth import AuthBearer
from .schemas import PostSchema, PostCreateSchema, ErrorSchema, PostUpdateSchema, NoneSchema
from .services import PostService

router = Router(tags=["posts"])


@router.get("/", response={
    200: List[PostSchema],
    403: ErrorSchema
}, auth=AuthBearer())
def list_posts(request):
    try:
        return PostService.get_posts()
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.get("/{post_id}", response={
    200: PostSchema,
    403: ErrorSchema
}, auth=AuthBearer())
def get_post(request,post_id: int):
    try:
        return PostService.get_post(post_id=post_id)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.post("/create", response={
    200: PostSchema,
    201: PostSchema,
    403: ErrorSchema
}, auth=AuthBearer())
def create_post(request, data: Form[PostCreateSchema]):
    try:
        return PostService.create_posts(request=request, data=data)
    except Exception as error:
        return Response({"error": str(error)}, status=500)

@router.patch("/{post_id}", response={
    200: PostSchema,
    403: ErrorSchema
}, auth=AuthBearer())
def update_post(request,post_id: int, data: PostUpdateSchema):
    try:
        return PostService.update_post(post_id=post_id ,payload=data)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.delete("/{post_id}", response={
    200: NoneSchema,
    403: ErrorSchema
}, auth=AuthBearer())
def delete_post(request,post_id: int):
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
def like_post(request, post_id: int = Path(...)):
    try:
        PostService.like_posts(request=request, post_id=post_id)
        return Response({"success": True}, status=200)
    except Exception as error:
        return Response({"error": str(error)}, status=500)
