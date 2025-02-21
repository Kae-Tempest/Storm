from apps.comments.models import Comment
from django.db.models import QuerySet


class CommentsServices:
    @staticmethod
    def get_comments() -> QuerySet[Comment]:
        return Comment.objects.all()
