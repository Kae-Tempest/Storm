from typing import List

from ninja import Router
from ninja.responses import Response

from .schemas import ErrorSchema, CommentSchema

from .services import CommentsServices

router = Router(tags=['comments'])


@router.get('/', response={
    200: List[CommentSchema],
    403: ErrorSchema
})
def comments_list(request):
    try:
        return CommentsServices.get_comments()
    except Exception as error:
        return Response({"message": str(error)}, status=500)
