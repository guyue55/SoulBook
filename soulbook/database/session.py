from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from soulbook.config.settings import settings


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Set to True to see SQL queries
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,  # Number of connection pools
    max_overflow=10,  # Additional connections beyond pool_size
)

# Create async session maker
AsyncSessionFactory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session():
    """
    Dependency function that provides a database session
    """
    async with AsyncSessionFactory() as session:
        yield session