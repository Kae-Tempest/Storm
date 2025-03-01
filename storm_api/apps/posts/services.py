from typing import Any

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from apps.posts.models import Post, PrivacyChoices
from apps.posts.schemas import PostCreateSchema, PostUpdateSchema


class PostService:
    @staticmethod
    def get_posts(request: HttpRequest) -> list[dict[str, Any | None]]:
        posts = (
            Post.objects.select_related("author")
            .prefetch_related("likes", "post_comments")
            .all()
        )
        posts_data = []
        for post in posts:
            # Construire l'URL complète
            if post.media_url:
                media_url = request.build_absolute_uri(post.media_url.url)
            else:
                media_url = None

            posts_data.append({
                "id": post.id,
                "content": post.content,
                "likes_count": post.likes_count,
                "comments_count": post.comments_count,
                "media_url": media_url,
                "is_liked": post.is_liked_by(request.user),
                "location": post.location,
                "privacy_setting": post.privacy_setting,
                "created_at": post.created_at,
                "number_of_shares": post.number_of_shares,
                "author": post.author
            })
        return posts_data

    @staticmethod
    def create_posts_raw(request, content, privacy_setting, media_url=None):
        """Version qui accepte des paramètres individuels plutôt qu'un objet schéma"""
        # Créer l'instance de Post
        user = request.user
        post = Post.objects.create(
            author=user,
            content=content,
            privacy_setting=privacy_setting
        )

        # Traiter le fichier si présent
        if media_url:
            # Gérer le fichier, peut-être le sauvegarder dans un stockage
            # Par exemple:
            post.media_url = media_url
            post.save()

        return post

    @staticmethod
    def get_post(request: HttpRequest, post_id: int) -> Post:
        post = (
            Post.objects.select_related("author")
            .prefetch_related("likes", "post_comments")
            .filter(id=post_id)
            .first()
        )
        if post.media_url:
            post.media_url = request.build_absolute_uri(post.media_url.url)
        else:
            post.media_url = None
        return post

    @staticmethod
    def create_posts(request: HttpRequest, data: PostCreateSchema) -> Post:
        post = Post(
            content=data.content,
            location=data.location,
            privacy_setting=data.privacy_setting,
            author=request.user,
        )

        if data.media_url:
            post.media_url.save(data.media_url.name, data.media_url)

        post.save()
        return post

    @staticmethod
    def update_post(post_id: int, payload: PostUpdateSchema) -> Post:
        posts = Post.objects.select_related("author").prefetch_related("likes")
        post = get_object_or_404(posts, id=post_id)

        data = payload.dict(exclude_unset=True)
        for attr, value in data.items():
            setattr(post, attr, value)

        post.save()
        return post

    @staticmethod
    def like_posts(request: HttpRequest, post_id: int) -> None:
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    @staticmethod
    def desactivate_post(post_id: int) -> None:
        post = get_object_or_404(Post, id=post_id)
        post.privacy_setting = PrivacyChoices.DELETED
        post.save()
