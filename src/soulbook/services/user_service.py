from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from soulbook.models.user import User
from soulbook.schemas.user import UserCreate, UserUpdate
from soulbook.database.crud.user import (
    get_user_by_id,
    get_user_by_username,
    create_user as crud_create_user,
    update_user as crud_update_user
)


async def get_user_by_id_service(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Service function to get user by ID
    """
    return await get_user_by_id(db, user_id)


async def get_user_by_username_service(db: AsyncSession, username: str) -> Optional[User]:
    """
    Service function to get user by username
    """
    return await get_user_by_username(db, username)


async def create_user_service(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Service function to create a new user
    """
    return await crud_create_user(db, user_data)


async def update_user_service(
    db: AsyncSession, user_id: int, user_data: UserUpdate
) -> Optional[User]:
    """
    Service function to update user information
    """
    return await crud_update_user(db, user_id, user_data)