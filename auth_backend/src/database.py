from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from schemas.config import settings


# Create the asynchronous engine with possible SSL configuration
async_engine = create_async_engine(settings.database_url, echo=False)

# Session factory configured to return asynchronous session instances
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Declarative base class for model classes
Base = declarative_base()


async def get_db():
    """Dependency that provides a session for FastAPI route functions."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        yield db
