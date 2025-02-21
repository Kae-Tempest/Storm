from apps.users.models import CustomUser
from django.db import models


class Comment(models.Model):
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="post_comments"
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        app_label = "comments"

    def __str__(self):
        return self.content
