from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from soulbook.database.session import get_db_session
from soulbook.database.crud.user import authenticate_user, create_user
from soulbook.schemas.user import UserCreate, UserInDB, Token
from soulbook.utils.security import create_access_token
from soulbook.config.settings import settings

router = APIRouter()


@router.post("/register", response_model=UserInDB)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db_session)):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = await authenticate_user(db, user_data.username, user_data.password)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_user = await create_user(db, user_data)
    return db_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    """
    Login to get access token
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}