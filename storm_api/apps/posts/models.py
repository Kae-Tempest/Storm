from django.db import models
from typing import Union

from apps.comments.models import Comment
from apps.users.models import CustomUser


class PrivacyChoices(models.TextChoices):
    PUBLIC = 'public', 'Public'
    FRIENDS_ONLY = 'friends_only', 'Friends Only'
    PRIVATE = 'private', 'Private'


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    content = models.TextField()
    title = models.CharField(max_length=255, null=True, blank=True)
    media_url = models.URLField(null=True, blank=True, db_index=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    privacy_setting = models.CharField(
        max_length=20,
        choices=PrivacyChoices,
        default=PrivacyChoices.PUBLIC
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    number_of_shares = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    @property
    def comments_count(self) -> int:
        return self.post_comments.count()

    def is_liked_by(self, user: Union[CustomUser, None]) -> bool:
        if user is None or not user.is_authenticated:
            return False
        return self.likes.filter(pk=user.id).exists()