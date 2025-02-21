from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .models import CustomUser


class UsersServices:
    @staticmethod
    def get_users() -> QuerySet[CustomUser]:
        return CustomUser.objects.all()

    @staticmethod
    def get_user_by_id(user_id: int) -> CustomUser:
        return CustomUser.objects.get(id=user_id)

    @staticmethod
    def get_user_by_email(email: str) -> CustomUser:
        return CustomUser.objects.get(email=email)

    @staticmethod
    def get_user_by_tag(tag: str) -> CustomUser:
        return CustomUser.objects.get(tag=tag)

    @staticmethod
    def update_user(user_id: int, payload) -> CustomUser:
        users = CustomUser.objects.all()
        user = get_object_or_404(users, id=user_id)

        data = payload.dict(exclude_unset=True)
        for attr, value in data.items():
            setattr(user, attr, value)

        user.save()
        return user

    @staticmethod
    def delete_user(user_id: int) -> None:
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
