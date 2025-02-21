from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router

from common.auth import AuthBearer
from .models import CustomUser
from .schemas import ErrorSchema, UserSchema, UserUpdateSchema
from .services import UsersServices

router = Router(tags=["users"])


@router.get("/", response={200: list[UserSchema], 403: ErrorSchema}, auth=AuthBearer())
def users_list(request: HttpRequest) -> QuerySet[CustomUser] | dict[str, str]:
    try:
        return UsersServices.get_users()
    except CustomUser.DoesNotExist:
        return {"message": "User not found"}


@router.get("/{user_id}", response={200: UserSchema, 403: ErrorSchema}, auth=AuthBearer())
def user_by_id(request: HttpRequest, user_id: int) -> CustomUser | dict[str, str]:
    try:
        return UsersServices.get_user_by_id(user_id=user_id)
    except CustomUser.DoesNotExist:
        return {"message": "User not found"}


@router.get("/email/{email}", response={200: UserSchema, 403: ErrorSchema}, auth=AuthBearer())
def user_by_email(request: HttpRequest, email: str) -> CustomUser | dict[str, str]:
    try:
        return UsersServices.get_user_by_email(email=email)
    except CustomUser.DoesNotExist:
        return {"message": "User not found"}


@router.get("/tag/{tag}", response={200: UserSchema, 403: ErrorSchema}, auth=AuthBearer())
def user_by_tag(request: HttpRequest, tag: str) -> CustomUser | dict[str, str]:
    try:
        return UsersServices.get_user_by_tag(tag=tag)
    except CustomUser.DoesNotExist:
        return {"message": "User not found"}


@router.patch("/{user_id}", response={200: UserSchema, 403: ErrorSchema}, auth=AuthBearer())
def user_patch(request: HttpRequest, user_id: int, payload: UserUpdateSchema) -> CustomUser | dict[str, str]:
    try:
        return UsersServices.update_user(user_id=user_id, payload=payload)
    except CustomUser.DoesNotExist:
        return {"message": "User not found"}


@router.delete("/{user_id}", response={200: dict[str, str], 403: ErrorSchema}, auth=AuthBearer())
def user_delete(request: HttpRequest, user_id: int) -> dict[str, str]:
    try:
        return UsersServices.delete_user(user_id=user_id)
    except CustomUser.DoesNotExist:
        return {"message": "User not found"}
