# apps/auth/api.py
from typing import cast

from django.http import HttpRequest
from ninja import Router
from ninja.errors import AuthenticationError
from ninja.responses import Response

from common.auth import AuthBearer
from .schemas import ErrorSchema, LoginSchema, TokenSchema, RegisterSchema, RegisterTokenSchema
from .services import AuthService
from ..users.models import CustomUser

router = Router(tags=["auth"])


@router.post("/login", response={200: TokenSchema, 401: ErrorSchema}, auth=None)
async def login(request: HttpRequest, payload: LoginSchema) -> dict[str, str] | Response:
    """Endpoint pour obtenir un token JWT"""
    try:
        return await AuthService.authenticate_user(
            email=payload.email, password=payload.password
        )
    except AuthenticationError as e:
        return Response({"detail": str(e)}, status=401)


@router.post("/register", response={200: RegisterTokenSchema, 401: ErrorSchema}, auth=None)
async def register(request: HttpRequest, payload: RegisterSchema) -> dict[str, str] | Response:
    try:
        return await AuthService.register_user(payload=payload)
    except AuthenticationError as e:
        return Response({"detail": str(e)}, status=401)


@router.post(
    "/token/refresh", response={200: TokenSchema, 401: ErrorSchema}, auth=AuthBearer()
)
async def refresh_token(request: HttpRequest) -> dict[str, str] | Response:
    """Endpoint pour rafraîchir un token JWT"""
    try:
        user = cast(CustomUser, request.user)
        return await AuthService.refresh_token(user)
    except AuthenticationError as e:
        return Response({"detail": str(e)}, status=401)


@router.get("/verify", response={200: dict, 401: ErrorSchema}, auth=AuthBearer())
async def verify_token(request: HttpRequest) -> dict[str, str] | ErrorSchema:
    """Endpoint pour vérifier la validité d'un token"""
    user = cast(CustomUser, request.user)
    return {"detail": "Token is valid", "user": user.username}
