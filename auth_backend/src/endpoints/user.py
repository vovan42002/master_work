from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from database import get_db
from auth.dependencies import get_current_user, is_admin_user
from models.user import UserModel
from schemas.user import UserCreateSchema, UserCreateResponseSchema, UserID
from crud.user import get_user_by_email, create_user, delete_user_by_id, get_user_by_id

router = APIRouter()


@router.post(
    "/users/",
    response_model=UserCreateResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
    _current_authenticated_user: UserModel = Depends(get_current_user),
    _current_user: UserModel = Depends(is_admin_user),
) -> Any:
    """
    Creates a new user in the system with specified details.
    """
    # Check if email is already registered
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user using CRUD function
    new_user = await create_user(db, user.model_dump())

    # Return formatted response
    return UserCreateResponseSchema.model_validate(new_user, from_attributes=True)


@router.delete(
    "/users/{user_id:int}",
    response_model=UserID,
    status_code=status.HTTP_201_CREATED,
)
async def block_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _current_authenticated_user: UserModel = Depends(get_current_user),
    _current_user: UserModel = Depends(is_admin_user),
) -> Any:
    """
    Creates a new user in the system with specified details.
    """
    # Check if email is already registered
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} is not registered",
        )

    # Create new user using CRUD function
    deleted_user_id = await delete_user_by_id(db, user_id)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} could not be deleted",
        )

    # Return the response in the format expected by UserID
    return UserID(id=deleted_user_id)
