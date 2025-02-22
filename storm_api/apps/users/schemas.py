from ninja import ModelSchema, Schema

from apps.users.models import CustomUser


class UserSchema(ModelSchema):
    class Meta:
        model = CustomUser
        db_table = "users"
        fields = "__all__"
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class UserUpdateSchema(Schema):
    display_name: str | None = None
    email: str | None = None
    avatar: str | None = None
    bio: str | None = None
    date_of_birth: str | None = None
    password: str | None = None


class ErrorSchema(Schema):
    message: str
