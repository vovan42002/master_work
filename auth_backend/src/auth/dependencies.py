import logging
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jwt import PyJWTError

from models.user import UserModel
from database import get_db
from auth.jwt_utils import JWTTokenHandler
from schemas.config import settings

logger = logging.getLogger(__name__)


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Cookie(None, alias="access_token")
) -> UserModel:
    """
    Retrieves the authenticated user based on a JWT token from cookies.

    Args:
        db: Database session for user data querying.
        token: JWT token for authentication.

    Returns:
        The authenticated UserModel instance or raises HTTPException for errors.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = JWTTokenHandler.verify_token(
            token,
            credentials_exception=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ),
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JWT token"
            )

        user_query = select(UserModel).filter(UserModel.email == email)
        result = await db.execute(user_query)
        user = result.scalars().first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token"
        )


async def is_admin_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Verifies if the authenticated user has admin privileges.

    Args:
        current_user: The authenticated UserModel instance.

    Returns:
        The UserModel if admin, otherwise raises HTTPException for insufficient privileges.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
