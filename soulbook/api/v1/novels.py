from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from soulbook.database.session import get_db_session
from soulbook.database.crud.novel import (
    get_novel_by_id, 
    get_novels_by_user, 
    search_novels, 
    create_novel, 
    get_bookmarks_by_user,
    create_bookmark
)
from soulbook.schemas.novel import NovelInDB, NovelCreate, NovelSearch, BookmarkInDB, BookmarkCreate
from soulbook.schemas.user import UserInDB
from soulbook.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[NovelInDB])
async def read_novels(
    current_user: UserInDB = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get novels for current user
    """
    novels = await get_novels_by_user(db, current_user.id, skip=skip, limit=limit)
    return novels


@router.post("/", response_model=NovelInDB)
async def create_novel_for_user(
    novel: NovelCreate,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Add a novel for the current user
    """
    # Check if novel already exists for this user
    existing_novel = await get_novels_by_user(db, current_user.id)
    for n in existing_novel:
        if n.title == novel.title and n.author == novel.author:
            raise HTTPException(status_code=400, detail="Novel already exists in your library")
    
    db_novel = await create_novel(db, novel, current_user.id)
    return db_novel


@router.get("/search", response_model=List[NovelInDB])
async def search_novels_endpoint(
    search_params: NovelSearch = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Search novels by keyword
    """
    novels = await search_novels(
        db, 
        search_params.keyword, 
        skip=(search_params.page - 1) * search_params.size, 
        limit=search_params.size
    )
    return novels


@router.get("/{novel_id}", response_model=NovelInDB)
async def read_novel(
    novel_id: int,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific novel
    """
    novel = await get_novel_by_id(db, novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    if novel.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return novel


@router.post("/bookmark", response_model=BookmarkInDB)
async def create_bookmark_endpoint(
    bookmark: BookmarkCreate,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create or update a bookmark for a novel
    """
    db_bookmark = await create_bookmark(db, bookmark, current_user.id)
    return db_bookmark


@router.get("/bookmarks", response_model=List[BookmarkInDB])
async def read_user_bookmarks(
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get all bookmarks for current user
    """
    bookmarks = await get_bookmarks_by_user(db, current_user.id)
    return bookmarks