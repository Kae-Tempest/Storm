from django.shortcuts import get_object_or_404

from apps.posts.models import Post
from apps.posts.schemas import PostCreateSchema, PostSchema, PostUpdateSchema


class PostService:
    @staticmethod
    def get_posts(request) -> list[PostCreateSchema]:
        posts = Post.objects.select_related('author').prefetch_related('likes')

        response = []
        for post in posts:
            post_data = PostSchema.from_orm(post, request_user=request.user)
            response.append(post_data)

        return response

    @staticmethod
    def create_posts(request, data: PostCreateSchema) -> Post:
        post = Post.objects.create(
            content=data.content,
            author=request.user
        )

        return PostSchema.from_orm(post, request_user=request.user)

    @staticmethod
    def like_posts(request, post_id: int):
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    @staticmethod
    def delete_post(request, post_id: int) -> None:
        post = get_object_or_404(Post, id=post_id)
        post.delete()

    @staticmethod
    def get_post(request, post_id: int) -> Post:
        post = get_object_or_404(Post, id=post_id)
        return PostSchema.from_orm(post, request_user=request.user)

    @staticmethod
    def update_post(request, post_id: int, data: PostUpdateSchema) -> Post:
        get_object_or_404(Post, id=post_id)

        post = Post.objects.update_or_create(
            id=post_id,
            content=data.content,
            author=request.user
        )

        return PostSchema.from_orm(post, request_user=request.user)