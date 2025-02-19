from django.db.models import QuerySet

from .models import CustomUser

class UsersServices:
    @staticmethod
    def get_users():
        return CustomUser.objects.all()