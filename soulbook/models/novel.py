from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Novel(Base):
    """Novel model"""
    
    title: Mapped[str] = mapped_column(String(255), index=True)
    author: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    cover_image_url: Mapped[str] = mapped_column(Text, nullable=True)
    source_url: Mapped[str] = mapped_column(Text)
    source_site: Mapped[str] = mapped_column(String(100))
    latest_chapter: Mapped[str] = mapped_column(String(255), nullable=True)
    latest_chapter_url: Mapped[str] = mapped_column(Text, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default="连载中")  # 连载中/已完结
    
    # Relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="novels")
    
    def __repr__(self) -> str:
        return f"<Novel(id={self.id}, title='{self.title}', author='{self.author}')>"


class NovelBookmark(Base):
    """Novel bookmark model"""
    
    novel_id: Mapped[int] = mapped_column(ForeignKey("novel.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    chapter_title: Mapped[str] = mapped_column(String(255))
    chapter_url: Mapped[str] = mapped_column(Text)
    read_progress: Mapped[float] = mapped_column(default=0.0)  # 阅读进度百分比
    
    # Relationships
    novel: Mapped["Novel"] = relationship(back_populates="bookmarks")
    user: Mapped["User"] = relationship(back_populates="bookmarks")
    
    def __repr__(self) -> str:
        return f"<Bookmark(user_id={self.user_id}, novel_id={self.novel_id})>"


# Add back_populates relationships to User model
User.novels = relationship("Novel", back_populates="user", cascade="all, delete-orphan")
User.bookmarks = relationship("NovelBookmark", back_populates="user", cascade="all, delete-orphan")

# Add back_populates relationship to Novel model
Novel.bookmarks = relationship("NovelBookmark", back_populates="novel", cascade="all, delete-orphan")