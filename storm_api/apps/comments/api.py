from apps.comments.models import Comment
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router
from ninja.responses import Response

from .schemas import CommentSchema, ErrorSchema
from .services import CommentsServices

router = Router(tags=["comments"])


@router.get("/", response={200: list[CommentSchema], 403: ErrorSchema})
def comments_list(request: HttpRequest) -> Response | QuerySet[Comment, Comment]:
    try:
        return CommentsServices.get_comments()
    except Exception as error:
        return Response({"message": str(error)}, status=500)
