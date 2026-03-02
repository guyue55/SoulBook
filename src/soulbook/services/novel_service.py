from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from soulbook.models.novel import Novel, NovelBookmark
from soulbook.schemas.novel import NovelCreate, NovelUpdate, BookmarkCreate
from soulbook.database.crud.novel import (
    get_novel_by_id,
    get_novels_by_user,
    search_novels,
    create_novel as crud_create_novel,
    update_novel as crud_update_novel,
    get_bookmarks_by_user,
    create_bookmark as crud_create_bookmark
)


async def get_novel_by_id_service(db: AsyncSession, novel_id: int) -> Optional[Novel]:
    """
    Service function to get novel by ID
    """
    return await get_novel_by_id(db, novel_id)


async def get_novels_by_user_service(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
) -> List[Novel]:
    """
    Service function to get novels by user ID
    """
    return await get_novels_by_user(db, user_id, skip, limit)


async def search_novels_service(
    db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100
) -> List[Novel]:
    """
    Service function to search novels by keyword
    """
    return await search_novels(db, keyword, skip, limit)


async def create_novel_service(
    db: AsyncSession, novel_data: NovelCreate, user_id: int
) -> Novel:
    """
    Service function to create a new novel
    """
    return await crud_create_novel(db, novel_data, user_id)


async def update_novel_service(
    db: AsyncSession, novel_id: int, novel_data: NovelUpdate
) -> Optional[Novel]:
    """
    Service function to update novel information
    """
    return await crud_update_novel(db, novel_id, novel_data)


async def get_user_bookmarks_service(
    db: AsyncSession, user_id: int
) -> List[NovelBookmark]:
    """
    Service function to get all bookmarks for a user
    """
    return await get_bookmarks_by_user(db, user_id)


async def create_bookmark_service(
    db: AsyncSession, bookmark_data: BookmarkCreate, user_id: int
) -> NovelBookmark:
    """
    Service function to create or update a bookmark
    """
    return await crud_create_bookmark(db, bookmark_data, user_id)