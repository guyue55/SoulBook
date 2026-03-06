from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc
from fastapi import HTTPException

from soulbook.models.novel import Novel, NovelBookmark
from soulbook.schemas.novel import NovelCreate, NovelUpdate, BookmarkCreate


async def get_novel_by_id(db: AsyncSession, novel_id: int) -> Optional[Novel]:
    """Get novel by ID"""
    result = await db.execute(select(Novel).filter(Novel.id == novel_id))
    return result.scalar_one_or_none()


async def get_novel_by_title_author(db: AsyncSession, title: str, author: str) -> Optional[Novel]:
    """Get novel by title and author"""
    result = await db.execute(
        select(Novel).filter(and_(Novel.title == title, Novel.author == author))
    )
    return result.scalar_one_or_none()


async def get_novels_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[Novel]:
    """Get novels by user ID"""
    result = await db.execute(
        select(Novel).filter(Novel.user_id == user_id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def search_novels(db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100) -> List[Novel]:
    """Search novels by keyword in title or author"""
    result = await db.execute(
        select(Novel).filter(
            and_(
                (Novel.title.contains(keyword)) | (Novel.author.contains(keyword)),
                Novel.is_deleted.is_(None)  # Assuming we might add soft delete later
            )
        ).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_novel(db: AsyncSession, novel_data: NovelCreate, user_id: int) -> Novel:
    """Create a new novel"""
    db_novel = Novel(**novel_data.model_dump(), user_id=user_id)
    
    db.add(db_novel)
    await db.commit()
    await db.refresh(db_novel)
    return db_novel


async def update_novel(db: AsyncSession, novel_id: int, novel_data: NovelUpdate) -> Optional[Novel]:
    """Update novel information"""
    db_novel = await get_novel_by_id(db, novel_id)
    if not db_novel:
        return None
    
    update_data = novel_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_novel, field, value)
    
    await db.commit()
    await db.refresh(db_novel)
    return db_novel


async def delete_novel(db: AsyncSession, novel_id: int) -> bool:
    """Delete a novel"""
    db_novel = await get_novel_by_id(db, novel_id)
    if not db_novel:
        return False
    
    await db.delete(db_novel)
    await db.commit()
    return True


async def get_bookmark_by_ids(db: AsyncSession, user_id: int, novel_id: int) -> Optional[NovelBookmark]:
    """Get bookmark by user_id and novel_id"""
    result = await db.execute(
        select(NovelBookmark).filter(
            and_(NovelBookmark.user_id == user_id, NovelBookmark.novel_id == novel_id)
        )
    )
    return result.scalar_one_or_none()


async def get_bookmarks_by_user(db: AsyncSession, user_id: int) -> List[NovelBookmark]:
    """Get all bookmarks for a user"""
    result = await db.execute(
        select(NovelBookmark).filter(NovelBookmark.user_id == user_id).order_by(desc(NovelBookmark.updated_at))
    )
    return result.scalars().all()


async def create_bookmark(db: AsyncSession, bookmark_data: BookmarkCreate, user_id: int) -> NovelBookmark:
    """Create a new bookmark"""
    # Check if bookmark already exists
    existing_bookmark = await get_bookmark_by_ids(db, user_id, bookmark_data.novel_id)
    if existing_bookmark:
        # Update existing bookmark
        for field, value in bookmark_data.model_dump().items():
            setattr(existing_bookmark, field, value)
        await db.commit()
        await db.refresh(existing_bookmark)
        return existing_bookmark
    
    # Create new bookmark
    db_bookmark = NovelBookmark(**bookmark_data.model_dump(), user_id=user_id)
    db.add(db_bookmark)
    await db.commit()
    await db.refresh(db_bookmark)
    return db_bookmark


async def delete_bookmark(db: AsyncSession, user_id: int, novel_id: int) -> bool:
    """Delete a bookmark"""
    db_bookmark = await get_bookmark_by_ids(db, user_id, novel_id)
    if not db_bookmark:
        return False
    
    await db.delete(db_bookmark)
    await db.commit()
    return True