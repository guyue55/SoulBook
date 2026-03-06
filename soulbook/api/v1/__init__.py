from fastapi import APIRouter

from . import auth, novels, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(novels.router, prefix="/novels", tags=["novels"])