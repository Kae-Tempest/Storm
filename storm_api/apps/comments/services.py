from .models import Comment

class CommentsServices:
    @staticmethod
    def get_comments():
        return Comment.objects.all()