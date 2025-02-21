from apps.posts.models import Post
from apps.posts.schemas import PostCreateSchema, PostUpdateSchema
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404


class PostService:
    @staticmethod
    def get_posts() -> QuerySet[Post]:
        posts = (
            Post.objects.select_related("author")
            .prefetch_related("likes", "post_comments")
            .all()
        )
        return posts

    @staticmethod
    def get_post(post_id: int) -> Post:
        post = (
            Post.objects.select_related("author")
            .prefetch_related("likes", "post_comments")
            .filter(id=post_id)
            .first()
        )
        return post

    @staticmethod
    def create_posts(request: HttpRequest, data: PostCreateSchema) -> Post:
        post = Post.objects.create(author=request.user, **data.dict())
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
    def delete_post(post_id: int) -> None:
        post = get_object_or_404(Post, id=post_id)
        post.delete()
