from config import get_settings
from fastapi import status
import httpx
import logging
from schemas import AuthAdapterUser


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


class AuthAdapter:
    def __init__(self, token: str):
        self.token = token

    async def get_user(self) -> AuthAdapterUser:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=f"{get_settings().application.auth_backend_base_url}/v1/users/me",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json",
                },
            )
            if resp.status_code != status.HTTP_200_OK:
                logger.error(
                    msg=f"Failed to get user by token from Auth susbsystem",
                    extra={"details": resp.json()},
                )
                resp.raise_for_status()
            return AuthAdapterUser(**resp.json())
