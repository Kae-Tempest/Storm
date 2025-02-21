from apps.users.models import CustomUser
from ninja import ModelSchema, Schema


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


class UserCreateSchema(Schema):
    username: str
    email: str
    avatar: str | None = None
    bio: str | None = None
    date_of_birth: str | None = None
    password: str
    confirm_password: str


class UserUpdateSchema(Schema):
    username: str | None = None
    email: str | None = None
    avatar: str | None = None
    bio: str | None = None
    date_of_birth: str | None = None
    password: str | None = None


class ErrorSchema(Schema):
    message: str
