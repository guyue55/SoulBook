from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from soulbook.database.session import get_db_session
from soulbook.database.crud.user import get_user_by_id
from soulbook.schemas.user import UserInDB
from soulbook.api.deps import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    """
    Get current user info
    """
    return current_user


@router.get("/{user_id}", response_model=UserInDB)
async def read_user(
    user_id: int, 
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get user by ID
    """
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user