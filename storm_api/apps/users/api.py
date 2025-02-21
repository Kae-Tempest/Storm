from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router

from .models import CustomUser
from .schemas import ErrorSchema, UserSchema
from .services import UsersServices

router = Router(tags=["users"])


@router.get("/", response={200: list[UserSchema], 403: ErrorSchema})
def users_list(request: HttpRequest) -> QuerySet[CustomUser] | dict[str, str]:
    try:
        return UsersServices.get_users()
    except CustomUser.DoesNotExist:
        return {"message": "User not found"}
