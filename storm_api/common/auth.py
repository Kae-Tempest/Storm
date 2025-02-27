from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import HttpRequest
from ninja.errors import AuthenticationError
from ninja.responses import Response
from ninja.security import HttpBearer

from apps.users.models import CustomUser


class AuthError(Exception):
    """Classe de base pour les erreurs d'authentification"""

    pass


class InvalidToken(AuthError):
    """Exception levée quand un token est invalide"""

    pass


class TokenExpired(AuthError):
    """Exception levée quand un token est expiré"""

    pass


class AuthBearer(HttpBearer):
    """
    Classe de gestion de l'authentification par token Bearer
    """

    async def authenticate(self, request: HttpRequest, token: str) -> str | None:
        """
        Authentifie un utilisateur à partir du token JWT.

        Args:
            request: La requête HTTP
            token: Le token JWT à valider

        Returns:
            Le token si valide, None sinon
        """
        if not token:
            return None

        try:
            # Clean up the token
            if token.lower().startswith("bearer"):
                token = token.split(" ", 1)[1].strip()

            # Décodage du token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Vérification de l'expiration
            exp = payload.get("exp")
            if not exp:
                raise InvalidToken("No expiration in token")

            if datetime.fromtimestamp(exp, tz=UTC) < datetime.now(tz=UTC):
                raise TokenExpired("Token has expired")

            # Récupération de l'utilisateur de façon asynchrone
            user_id = payload.get("user_id")
            if not user_id:
                raise InvalidToken("No user_id in token")

            # Wrap the database query in sync_to_async
            get_user = sync_to_async(CustomUser.objects.filter(id=user_id).first)
            user = await get_user()

            if datetime.fromtimestamp(exp, tz=UTC) - timedelta(minutes=10) < datetime.now(
                    tz=UTC) and datetime.fromtimestamp(exp, tz=UTC) > datetime.now(tz=UTC):
                try:
                    token = create_token(user)
                except Exception as e:
                    raise AuthenticationError(f"Token refresh failed: {str(e)}")

            if not user:
                raise InvalidToken("User not found")

            if not user.is_active:
                raise InvalidToken("User is inactive")

            # Ajout de l'utilisateur à la requête
            request.user = user
            return token

        except jwt.ExpiredSignatureError:
            Response({"detail": "Token has expired"}, status=403)
            raise TokenExpired("Token has expired")
        except jwt.InvalidTokenError as e:
            Response({"detail": "Invalid token format"}, status=500)
            raise InvalidToken(f"Invalid token format: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


def create_token(user: CustomUser, expiration: timedelta | None = None) -> str:
    """
    Crée un token JWT pour un utilisateur.

    Args:
        user: L'utilisateur pour lequel créer le token
        expiration: Durée de validité du token (par défaut 1 jour)

    Returns:
        Le token JWT encodé

    Raises:
        ValueError: Si l'utilisateur n'est pas valide
    """
    if not user.is_active:
        raise ValueError("Cannot create token for inactive user")

    if expiration is None:
        expiration = timedelta(days=1)

    current_time = datetime.now(tz=UTC)
    exp_time = current_time + expiration

    payload = {
        "user_id": str(user.id),
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "iat": int(current_time.timestamp()),
        "exp": int(exp_time.timestamp()),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token


def decode_token(token: str) -> Any:
    """
    Décode un token JWT.

    Args:
        token: Le token JWT à décoder

    Returns:
        Le contenu décodé du token

    Raises:
        InvalidToken: Si le token est invalide
        TokenExpired: Si le token est expiré
    """
    if not token:
        raise InvalidToken("Token is required")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpired("Token has expired")
    except jwt.PyJWTError as e:
        raise InvalidToken(f"Invalid token: {str(e)}")


def validate_token(token: str) -> bool:
    """
    Vérifie si un token est valide.

    Args:
        token: Le token JWT à vérifier

    Returns:
        True si le token est valide, False sinon
    """
    try:
        decode_token(token)
        return True
    except (InvalidToken, TokenExpired):
        return False


def get_token_expiration(token: str) -> datetime | None:
    """
    Retourne la date d'expiration d'un token.

    Args:
        token: Le token JWT

    Returns:
        La date d'expiration ou None si le token est invalide
    """
    try:
        payload = decode_token(token)
        exp = payload.get("exp")
        if exp:
            return datetime.fromtimestamp(exp, tz=UTC)
        return None
    except (InvalidToken, TokenExpired):
        return None
