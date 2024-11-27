from pydantic import BaseModel


class AccessToken(BaseModel):
    token: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenResponse(AccessToken, RefreshToken):
    pass
