from typing import List

from ninja import Router
from ninja.responses import Response
from .schemas import ErrorSchema, UserSchema

from .models import CustomUser
from .services import UsersServices

router = Router(tags=['users'])


@router.get('/', response={
    200: List[UserSchema],
    403: ErrorSchema
})
def users_list(request):
    try:
        return UsersServices.get_users()
    except CustomUser.DoesNotExist:
        return {'message': 'User not found'}
