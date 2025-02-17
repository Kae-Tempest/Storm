# apps/auth/api.py
from ninja import Router
from ninja.errors import AuthenticationError
from ninja.responses import Response

from .schemas import TokenSchema, LoginSchema, ErrorSchema
from .services import AuthService
from common.auth import AuthBearer

router = Router(tags=["auth"])


@router.post("/login", response={200: TokenSchema, 401: ErrorSchema}, auth=None)
async def login(request, payload: LoginSchema):
    """Endpoint pour obtenir un token JWT"""
    try:
        return await AuthService.authenticate_user(
            email=payload.email,
            password=payload.password
        )
    except AuthenticationError as e:
        return Response({"detail": str(e)}, status=401)


@router.post("/token/refresh", response={200: TokenSchema, 401: ErrorSchema}, auth=AuthBearer())
async def refresh_token(request):
    """Endpoint pour rafraîchir un token JWT"""
    try:
        return await AuthService.refresh_token(request.user)
    except AuthenticationError as e:
        return Response({"detail": str(e)}, status=401)


@router.get("/verify", response={200: dict, 401: ErrorSchema}, auth=AuthBearer())
async def verify_token(request):
    """Endpoint pour vérifier la validité d'un token"""
    return {"detail": "Token is valid", "user": request.user.username}
