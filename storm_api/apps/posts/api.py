from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router, Form
from ninja.responses import Response

from common.auth import AuthBearer
from .models import Post
from .schemas import (
    ErrorSchema,
    PostSchema, PostUpdateSchema, NoneSchema, PostOutSchema,
)
from .services import PostService

router = Router(tags=["posts"])


@router.get("/", response={200: list[PostOutSchema], 403: ErrorSchema}, auth=AuthBearer())
def list_posts(request: HttpRequest) -> QuerySet[Post] | Response:
    try:
        return PostService.get_posts(request)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.get(
    "/{int:post_id}", response={200: PostOutSchema, 403: ErrorSchema}, auth=AuthBearer()
)
def get_post(request: HttpRequest, post_id: int) -> Post | Response:
    try:
        return PostService.get_post(request, post_id=post_id)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.post(
    "/",
    response={200: PostSchema, 201: PostSchema, 403: ErrorSchema},
    auth=AuthBearer(),
)
def create_post(
        request: HttpRequest,
        content: str = Form(...),
        privacy_setting: str = Form(...)
) -> Post | Response:
    try:
        # Accéder directement au fichier depuis request.FILES
        media_url = request.FILES.get('media_url')

        # Créer un dictionnaire avec les données du formulaire
        post_data = {
            "content": content,
            "privacy_setting": privacy_setting
        }

        # Ajouter le fichier seulement s'il existe
        if media_url is not None:
            post_data["media_url"] = media_url

        # Logs détaillés pour débogage
        print(f"Type de media_url: {type(media_url)}")
        print(f"Post data: {post_data}")

        # Créer l'objet du service sans passer par le schéma Pydantic
        # Adaptez cette partie selon l'implémentation de votre PostService
        post = PostService.create_posts_raw(
            request=request,
            content=content,
            privacy_setting=privacy_setting,
            media_url=media_url
        )

        return post
    except Exception as error:
        print(f"Erreur lors de la création du post: {error}")
        import traceback
        traceback.print_exc()
        return Response({"error": str(error)}, status=500)


@router.patch(
    "/{int:post_id}", response={200: PostSchema, 403: ErrorSchema}, auth=AuthBearer()
)
def update_post(request: HttpRequest, post_id: int, data: PostUpdateSchema) -> Post | Response:
    try:
        return PostService.update_post(post_id=post_id, payload=data)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.delete(
    "/{int:post_id}", response={200: NoneSchema, 403: ErrorSchema}, auth=AuthBearer()
)
def delete_post(request: HttpRequest, post_id: int) -> dict[str, bool] | Response:
    try:
        PostService.desactivate_post(post_id=post_id)
        return {"success": True}
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@router.post("/{int:post_id}/like", response={
    200: NoneSchema,
    403: ErrorSchema,
    404: ErrorSchema
}, auth=AuthBearer())
def like_post(request: HttpRequest, post_id: int) -> NoneSchema | Response:
    try:
        PostService.like_posts(request=request, post_id=post_id)
        return Response({"success": True}, status=200)
    except Exception as error:
        return Response({"error": str(error)}, status=500)
