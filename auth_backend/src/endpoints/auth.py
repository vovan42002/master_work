import logging
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import PyJWTError

from database import get_db
from auth import password_utils
from auth.jwt_utils import JWTTokenHandler
from crud.user import get_user_by_email
from schemas.auth import AccessToken, TokenResponse

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)


router = APIRouter()
security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Authenticate a user and return JWT access and refresh tokens."""

    user = await get_user_by_email(db, form_data.username)

    if not user or not password_utils.verify_password(
        form_data.password, user.password_hash
    ):
        logger.warning(f"Failed login attempt for email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = JWTTokenHandler.create_access_token(data={"sub": user.email})
    refresh_token = JWTTokenHandler.create_refresh_token(data={"sub": user.email})

    logger.info(f"User {form_data.username} logged in successfully.")
    return TokenResponse(
        token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh_token")
async def refresh_token(
    refresh_token: HTTPAuthorizationCredentials = Depends(security),
):
    """Refreshes an access token using a valid refresh token provided as an HTTP-only cookie."""

    if refresh_token is None:
        logger.warning("Attempt to refresh token without a refresh token cookie.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_email = JWTTokenHandler.verify_token(
            refresh_token.credentials,
            credentials_exception=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ),
        )["sub"]

        new_access_token = JWTTokenHandler.create_access_token(data={"sub": user_email})

        logger.info(f"Access token refreshed successfully for user {user_email}.")
        return AccessToken(token=new_access_token)

    except PyJWTError:
        logger.error("Invalid refresh token attempt.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
