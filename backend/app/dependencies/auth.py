from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.exceptions import AuthenticationException


# Extracts JWT from:
# Authorization: Bearer <token>
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency to extract and validate JWT access token
    from the Authorization header.

    Returns authenticated User model or raises HTTP 401.
    """

    if not credentials:
        raise AuthenticationException(
            "Authentication required. Please log in."
        )

    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise AuthenticationException(
            "Invalid or expired authentication token."
        )

    user_id_str = payload.get("sub")

    if not user_id_str or not user_id_str.isdigit():
        raise AuthenticationException(
            "Invalid token payload format."
        )

    user_id = int(user_id_str)

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise AuthenticationException(
            "User account associated with token no longer exists."
        )

    return user