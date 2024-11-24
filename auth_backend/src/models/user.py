from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base
from auth.password_utils import pwd_context


class UserModel(Base):
    """
    Represents a user within the application, storing authentication and profile information.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(
        String(255), nullable=False
    )  # Ensure hash length fits algorithm used
    name = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def verify_password(self, password: str) -> bool:
        """
        Verify a password against the stored password hash.
        """
        return pwd_context.verify(password, self.password_hash)

    @property
    def username(self) -> str:
        """Alias for email as username."""
        return self.email

    @username.setter
    def username(self, value: str) -> None:
        self.email = value
