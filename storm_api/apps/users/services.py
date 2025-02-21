from django.db.models import QuerySet

from .models import CustomUser

class UsersServices:
    @staticmethod
    def get_users():
        return CustomUser.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        return CustomUser.objects.get(id=user_id)

    @staticmethod
    def get_user_by_email(email):
        return CustomUser.objects.get(email=email)

    @staticmethod
    def get_user_by_tag(tag):
        return CustomUser.objects.get(tag=tag)

    @staticmethod
    def update_user(user_id):
        user = CustomUser.objects.get(id=user_id)
    