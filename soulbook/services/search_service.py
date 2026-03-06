from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from soulbook.models.novel import Novel
from soulbook.database.crud.novel import search_novels


async def global_search_novels(
    db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100
) -> List[Novel]:
    """
    Global search function for novels
    """
    return await search_novels(db, keyword, skip, limit)


async def recommend_novels_by_user_history(
    db: AsyncSession, user_id: int, limit: int = 10
) -> List[Novel]:
    """
    Recommend novels based on user reading history
    This is a basic implementation - in a real system you'd implement
    more sophisticated recommendation algorithms
    """
    # This would typically involve more complex logic like:
    # 1. Analyzing user's reading history
    # 2. Finding similar novels based on genre, author, etc.
    # 3. Using collaborative filtering techniques
    
    # For now, return popular novels as recommendations
    # In a real implementation, this would use ML algorithms
    popular_novels = await search_novels(db, "", skip=0, limit=limit)
    return popular_novels