import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from soulbook.services.novel_service import (
    get_novel_by_id_service,
    get_novels_by_user_service,
    search_novels_service,
    create_novel_service
)
from soulbook.services.user_service import (
    get_user_by_id_service,
    get_user_by_username_service,
    create_user_service
)
from soulbook.models.novel import Novel
from soulbook.models.user import User
from soulbook.schemas.novel import NovelCreate
from soulbook.schemas.user import UserCreate


@pytest.mark.asyncio
class TestNovelService:
    async def test_get_novel_by_id_service(self):
        # Mock the database call
        mock_db = AsyncMock(spec=AsyncSession)
        expected_novel = Novel(
            id=1,
            title="Test Novel",
            author="Test Author",
            source_url="http://example.com",
            source_site="test_site",
            user_id=1
        )
        
        # Mock the get_novel_by_id function to return our expected novel
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("soulbook.services.novel_service.get_novel_by_id", AsyncMock(return_value=expected_novel))
            result = await get_novel_by_id_service(mock_db, 1)
        
        assert result == expected_novel

    async def test_get_novels_by_user_service(self):
        # Mock the database call
        mock_db = AsyncMock(spec=AsyncSession)
        expected_novels = [
            Novel(
                id=1,
                title="Test Novel 1",
                author="Test Author 1",
                source_url="http://example1.com",
                source_site="test_site",
                user_id=1
            ),
            Novel(
                id=2,
                title="Test Novel 2",
                author="Test Author 2",
                source_url="http://example2.com",
                source_site="test_site",
                user_id=1
            )
        ]
        
        # Mock the get_novels_by_user function
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("soulbook.services.novel_service.get_novels_by_user", AsyncMock(return_value=expected_novels))
            result = await get_novels_by_user_service(mock_db, 1)
        
        assert result == expected_novels
        assert len(result) == 2

    async def test_search_novels_service(self):
        # Mock the database call
        mock_db = AsyncMock(spec=AsyncSession)
        expected_novels = [
            Novel(
                id=1,
                title="Test Novel",
                author="Test Author",
                source_url="http://example.com",
                source_site="test_site",
                user_id=1
            )
        ]
        
        # Mock the search_novels function
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("soulbook.services.novel_service.search_novels", AsyncMock(return_value=expected_novels))
            result = await search_novels_service(mock_db, "test_keyword")
        
        assert result == expected_novels
        assert result[0].title == "Test Novel"

    async def test_create_novel_service(self):
        # Mock the database call
        mock_db = AsyncMock(spec=AsyncSession)
        novel_data = NovelCreate(
            title="New Novel",
            author="New Author",
            source_url="http://newnovel.com",
            source_site="test_site"
        )
        expected_novel = Novel(
            id=1,
            title=novel_data.title,
            author=novel_data.author,
            source_url=novel_data.source_url,
            source_site=novel_data.source_site,
            user_id=1
        )
        
        # Mock the crud_create_novel function
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("soulbook.services.novel_service.crud_create_novel", AsyncMock(return_value=expected_novel))
            result = await create_novel_service(mock_db, novel_data, 1)
        
        assert result == expected_novel
        assert result.title == "New Novel"


@pytest.mark.asyncio
class TestUserService:
    async def test_get_user_by_id_service(self):
        # Mock the database call
        mock_db = AsyncMock(spec=AsyncSession)
        expected_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        # Mock the get_user_by_id function
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("soulbook.services.user_service.get_user_by_id", AsyncMock(return_value=expected_user))
            result = await get_user_by_id_service(mock_db, 1)
        
        assert result == expected_user
        assert result.username == "testuser"

    async def test_get_user_by_username_service(self):
        # Mock the database call
        mock_db = AsyncMock(spec=AsyncSession)
        expected_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        # Mock the get_user_by_username function
        with pytest.Mock.patch("soulbook.services.user_service.get_user_by_username", new_callable=AsyncMock) as mock_func:
            mock_func.return_value = expected_user
            result = await get_user_by_username_service(mock_db, "testuser")
        
        assert result == expected_user
        assert result.email == "test@example.com"

    async def test_create_user_service(self):
        # Mock the database call
        mock_db = AsyncMock(spec=AsyncSession)
        user_data = UserCreate(
            username="newuser",
            email="new@example.com",
            password="newpassword"
        )
        expected_user = User(
            id=1,
            username=user_data.username,
            email=user_data.email,
            hashed_password="hashed_password"
        )
        
        # Mock the crud_create_user function
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("soulbook.services.user_service.crud_create_user", AsyncMock(return_value=expected_user))
            result = await create_user_service(mock_db, user_data)
        
        assert result == expected_user
        assert result.username == "newuser"