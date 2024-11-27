import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings

logger = logging.getLogger(__name__)


security = HTTPBearer()


def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify that the provided API access token is valid.
    """

    if credentials.credentials != settings.access_token:
        logger.warning("Invalid token from request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return True
