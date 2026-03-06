"""
Script to initialize the database with tables and sample data
"""
import asyncio
import sys
import os

# Add the src directory to the path so we can import soulbook modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from soulbook.models.base import Base
from soulbook.config.settings import settings


async def init_db():
    """
    Initialize the database by creating all tables
    """
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    # Dispose the engine
    await engine.dispose()
    
    print("Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())