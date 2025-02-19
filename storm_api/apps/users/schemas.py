from ninja import ModelSchema, Schema

from apps.users.models import CustomUser


class UserSchema(ModelSchema):
    class Meta:
        model = CustomUser
        fields = "__all__"
        exclude = ("password",'last_login', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

class ErrorSchema(Schema):
    message: str