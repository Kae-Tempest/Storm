# apps/auth/services.py
from datetime import timedelta
from typing import cast

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from ninja.errors import AuthenticationError

from apps.authentication.schemas import RegisterSchema
from apps.users.models import CustomUser
from common.auth import InvalidToken, TokenExpired, create_token, decode_token


class AuthService:
    @staticmethod
    async def authenticate_user(email: str, password: str) -> dict[str, str]:
        """
        Authentifie un utilisateur et retourne le token si les credentials sont valides.
        """
        try:
            # Wrap the synchronous authenticate function
            user = await sync_to_async(authenticate)(email=email, password=password)

            if not user:
                raise AuthenticationError("Invalid credentials")

            if not user.is_active:
                raise AuthenticationError("User account is disabled")

            # Wrap the synchronous database query
            user = cast(CustomUser, user)
            user_obj = await sync_to_async(CustomUser.objects.get)(id=user.id)

            # If create_token is synchronous, wrap it too
            token = await sync_to_async(create_token)(
                user=user_obj, expiration=timedelta(hours=2)
            )

            return {"access_token": token, "token_type": "bearer"}

        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}")

    @staticmethod
    async def verify_token(token: str) -> CustomUser | None:
        """
        Vérifie la validité d'un token et retourne l'utilisateur associé.
        """
        try:
            payload = decode_token(token)
            user = CustomUser.objects.filter(username=payload["username"]).first()
            return user
        except TokenExpired:
            raise AuthenticationError("Token has expired")
        except InvalidToken:
            raise AuthenticationError("Invalid token")

    @staticmethod
    async def refresh_token(user: CustomUser) -> dict[str, str]:
        """
        Génère un nouveau token pour un utilisateur.
        """
        try:
            new_token = create_token(user)
            return {"access_token": new_token, "token_type": "bearer"}
        except Exception as e:
            raise AuthenticationError(f"Token refresh failed: {str(e)}")

    @staticmethod
    async def register_user(payload: RegisterSchema) -> dict[str, str]:
        """
        Enregistre un utilisateur, authentifie l'utilisateur et retourne le token
        """
        try:
            await sync_to_async(CustomUser.objects.create_user)(
                payload.email,
                payload.username,
                payload.password,
                display_name=payload.display_name.lower()
            )

            user = await sync_to_async(authenticate)(email=payload.email, password=payload.password)

            if not user:
                raise AuthenticationError("Invalid credentials")

            if not user.is_active:
                raise AuthenticationError("User account is disabled")

            # Wrap the synchronous database query
            user = cast(CustomUser, user)
            user_obj = await sync_to_async(CustomUser.objects.get)(id=user.id)

            # If create_token is synchronous, wrap it too
            token = await sync_to_async(create_token)(
                user=user_obj, expiration=timedelta(hours=2)
            )
            return {"access_token": token, "token_type": "bearer", "user": user_obj}
        except Exception as e:
            raise AuthenticationError(f"Token registration failed: {str(e)}")
