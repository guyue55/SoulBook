from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NovelBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    source_url: str
    source_site: str
    latest_chapter: Optional[str] = None
    latest_chapter_url: Optional[str] = None
    word_count: Optional[int] = 0
    status: Optional[str] = "连载中"  # 连载中/已完结


class NovelCreate(NovelBase):
    pass


class NovelUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    latest_chapter: Optional[str] = None
    latest_chapter_url: Optional[str] = None
    status: Optional[str] = None


class NovelInDB(NovelBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NovelSearch(BaseModel):
    keyword: str
    page: int = 1
    size: int = 20


class Chapter(BaseModel):
    title: str
    url: str
    content: Optional[str] = None


class BookmarkBase(BaseModel):
    novel_id: int
    chapter_title: str
    chapter_url: str
    read_progress: float = 0.0


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkInDB(BookmarkBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True