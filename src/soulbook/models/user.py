from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .novel import Novel


class User(Base):
    """User model"""
    
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"