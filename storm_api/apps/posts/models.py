from django.db import models
from typing import Union
from apps.users.models import CustomUser

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    def is_liked_by(self, user: Union[CustomUser]) -> bool:
        if user is None or not user.is_authenticated:
            return False
        return self.likes.filter(pk=user.id).exists()