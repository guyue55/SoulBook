import pytest
from datetime import datetime
from soulbook.models.user import User
from soulbook.models.novel import Novel, NovelBookmark
from soulbook.models.base import Base


class TestUserModel:
    def test_user_creation(self):
        """Test creating a user instance"""
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password"
        assert user.is_active is True  # Default value
        assert user.is_superuser is False  # Default value

    def test_user_repr(self):
        """Test user representation"""
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        expected_repr = "<User(id=1, username='testuser')>"
        assert repr(user) == expected_repr


class TestNovelModel:
    def test_novel_creation(self):
        """Test creating a novel instance"""
        novel = Novel(
            title="Test Novel",
            author="Test Author",
            description="A test novel",
            source_url="http://example.com",
            source_site="test_site",
            user_id=1
        )
        
        assert novel.title == "Test Novel"
        assert novel.author == "Test Author"
        assert novel.description == "A test novel"
        assert novel.source_url == "http://example.com"
        assert novel.source_site == "test_site"
        assert novel.user_id == 1
        assert novel.status == "连载中"  # Default value

    def test_novel_repr(self):
        """Test novel representation"""
        novel = Novel(
            id=1,
            title="Test Novel",
            author="Test Author",
            description="A test novel",
            source_url="http://example.com",
            source_site="test_site",
            user_id=1
        )
        
        expected_repr = "<Novel(id=1, title='Test Novel', author='Test Author')>"
        assert repr(novel) == expected_repr


class TestNovelBookmarkModel:
    def test_bookmark_creation(self):
        """Test creating a bookmark instance"""
        bookmark = NovelBookmark(
            novel_id=1,
            user_id=1,
            chapter_title="Chapter 1",
            chapter_url="http://example.com/chapter1",
            read_progress=0.5
        )
        
        assert bookmark.novel_id == 1
        assert bookmark.user_id == 1
        assert bookmark.chapter_title == "Chapter 1"
        assert bookmark.chapter_url == "http://example.com/chapter1"
        assert bookmark.read_progress == 0.5

    def test_bookmark_repr(self):
        """Test bookmark representation"""
        bookmark = NovelBookmark(
            novel_id=1,
            user_id=1,
            chapter_title="Chapter 1",
            chapter_url="http://example.com/chapter1",
            read_progress=0.5
        )
        
        expected_repr = "<Bookmark(user_id=1, novel_id=1)>"
        assert repr(bookmark) == expected_repr


class TestBaseModel:
    def test_base_model_properties(self):
        """Test base model properties are inherited correctly"""
        # Check that the table name is derived from class name
        assert User.__tablename__ == 'user'
        assert Novel.__tablename__ == 'novel'
        assert NovelBookmark.__tablename__ == 'novelbookmark'
        
        # Check that id field exists
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        assert hasattr(user, 'id')
        
        # Check that timestamps exist
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')