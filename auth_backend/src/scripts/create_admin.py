import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import AsyncSessionLocal as SessionLocal
from models.user import UserModel
from auth.password_utils import hash_password
from schemas.config import settings

from contextlib import asynccontextmanager
from fastapi import FastAPI

# Set up logging
log_level = logging.DEBUG
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)


async def check_admin_exists(db_session, email) -> bool:
    try:
        result = await db_session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none() is not None
    except SQLAlchemyError as e:
        logger.error(f"Error checking admin existence: {e}")
        return False


async def create_admin_user(db_session, email, name, password):
    try:
        hashed_password = hash_password(password)
        admin_user = UserModel(
            email=email, password_hash=hashed_password, name=name, is_admin=True
        )
        db_session.add(admin_user)
        await db_session.commit()
        await db_session.refresh(admin_user)
        logger.info(f"Admin user {email} created successfully.")
    except SQLAlchemyError as e:
        await db_session.rollback()  # Rollback in case of an error
        logger.error(f"Failed to create admin user: {e}")


async def main():
    async with SessionLocal() as db:
        if await check_admin_exists(db, settings.admin_email):
            logger.info("Admin user already exists.")
        else:
            await create_admin_user(
                db, settings.admin_email, settings.admin_name, settings.admin_password
            )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await main()
    yield
