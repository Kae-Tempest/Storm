from django.db import models

from apps.posts.models import Post
from apps.users.models import CustomUser


class PrivacyChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    DELETED = "deleted", "Deleted"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=PrivacyChoices.choices, default=PrivacyChoices.ACTIVE
    )

    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    edited_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_comments", blank=True)
    reportes = models.ManyToManyField(CustomUser, related_name="reported_comments", blank=True)

    class Meta:
        ordering = ["-created_at"]
        app_label = "comments"

    def __str__(self):
        return self.content

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    @property
    def reportes_count(self) -> int:
        return self.reportes.count()

    def is_liked_by(self, user: CustomUser | None) -> bool:
        if user is None or not user.is_authenticated:
            return False
        return self.likes.filter(pk=user.id).exists()

    def is_reported_by(self, user: CustomUser | None) -> bool:
        if user is None or not user.is_authenticated:
            return False
        return self.reportes.filter(pk=user.id).exists()
