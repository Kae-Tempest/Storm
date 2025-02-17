from ninja import Schema

class UserSchema(Schema):
    id: int
    username: str

    @classmethod
    def from_orm(cls, user, **kwargs):
        return cls(
            id=user.id,
            username=user.username,
        )

class ErrorSchema(Schema):
    message: str