from pydantic_settings import BaseSettings
from pydantic import EmailStr, Field


class Settings(BaseSettings):
    """
    Application configuration settings derived from environment variables.
    """

    database_url: str
    # Essential JWT settings
    secret_key: str = Field(..., description="Secret key for JWT encoding")
    algorithm: str = "HS256"
    access_token_expires_delta: int = 30
    refresh_token_expires_delta: int = 1440

    # Admin user configuration
    admin_email: EmailStr
    admin_password: str
    admin_name: str = "Admin"

    # Server configuration
    use_ssl: bool = Field(True, description="Enable SSL for secure connections")
    secure_cookie: bool = Field(True, description="Enable secure cookies")
    log_level: str = "ERROR"


settings = Settings()
