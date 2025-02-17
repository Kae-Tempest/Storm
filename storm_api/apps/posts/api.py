from ninja import Path, Router
from typing import List

from ninja.responses import Response

from common.auth import AuthBearer
from .schemas import PostSchema, PostCreateSchema, ErrorSchema, PostUpdateSchema
from .services import PostService

router = Router(tags=["posts"])


@router.get("/", response={
    200: List[PostSchema],
    403: ErrorSchema
}, auth=AuthBearer())
def list_posts(request):
    try:
        return Response(PostService.get_posts(request), status=200)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.get("/{post_id}", response={
    200: PostSchema,
    403: ErrorSchema
}, auth=AuthBearer())
def get_post(request, post_id: int):
    try:
        return Response(PostService.get_post(request=request, post_id=post_id), status=200)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.post("/create", response={
    201: PostSchema,
    403: ErrorSchema
}, auth=AuthBearer())
def create_post(request, data: PostCreateSchema):
    try:
        post = PostService.create_posts(request=request, data=data)
        return Response(post, status=201)
    except Exception as error:
        return Response({"error": str(error)}, status=500)

@router.patch("/{post_id}", response={
    200: PostSchema,
    403: ErrorSchema
}, auth=AuthBearer())
def update_post(request,post_id: int, data: PostUpdateSchema):
    try:
        return Response(PostService.update_post(request=request, post_id=post_id ,data=data))
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.delete("/{post_id}", response={
    204: None,
    403: ErrorSchema
}, auth=AuthBearer())
def delete_post(request, post_id: int):
    try:
        PostService.delete_post(request=request, post_id=post_id)
        return Response({}, status=204)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.post("/{post_id}/like", response={
    200: None,
    403: ErrorSchema,
    404: ErrorSchema
}, auth=AuthBearer())
def like_post(request, post_id: int = Path(...)):
    try:
        PostService.like_posts(request=request, post_id=post_id)
        return Response({"success": True}, status=200)
    except Exception as error:
        return Response({"error": str(error)}, status=500)
