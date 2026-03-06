"""
Data migration script to migrate data from old MongoDB to new PostgreSQL
"""
import asyncio
import sys
import os
from typing import List, Dict

# Add the src directory to the path so we can import soulbook modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClient
from soulbook.models.user import User
from soulbook.models.novel import Novel
from soulbook.database.session import AsyncSessionFactory
from soulbook.utils.security import hash_password


class DataMigration:
    def __init__(self, mongodb_uri: str, postgresql_uri: str):
        self.mongodb_client = AsyncIOMotorClient(mongodb_uri)
        self.mongodb_db = self.mongodb_client.get_database("owllook")
        self.postgresql_uri = postgresql_uri

    async def migrate_users(self):
        """
        Migrate users from MongoDB to PostgreSQL
        """
        print("Starting user migration...")
        
        # Get all users from MongoDB
        mongodb_users = self.mongodb_db.get_collection("users")
        cursor = mongodb_users.find({})
        old_users = await cursor.to_list(length=None)
        
        migrated_count = 0
        async with AsyncSessionFactory() as db_session:
            for old_user in old_users:
                # Check if user already exists
                existing_user = await self.get_user_by_username(db_session, old_user.get('username'))
                if existing_user:
                    continue
                
                # Create new user
                new_user = User(
                    username=old_user.get('username', ''),
                    email=old_user.get('email', ''),
                    hashed_password=hash_password(old_user.get('password', '')),
                    is_active=old_user.get('is_active', True),
                    is_superuser=old_user.get('is_superuser', False)
                )
                
                db_session.add(new_user)
                try:
                    await db_session.commit()
                    await db_session.refresh(new_user)
                    migrated_count += 1
                    print(f"Migrated user: {old_user.get('username')}")
                except Exception as e:
                    print(f"Error migrating user {old_user.get('username')}: {e}")
                    await db_session.rollback()
        
        print(f"User migration completed. Total migrated: {migrated_count}")

    async def get_user_by_username(self, db_session: AsyncSession, username: str) -> User:
        """
        Helper function to check if user already exists
        """
        result = await db_session.execute(User.__table__.select().where(User.username == username))
        return result.first()

    async def migrate_novels(self):
        """
        Migrate novels from MongoDB to PostgreSQL
        """
        print("Starting novel migration...")
        
        # Get all novels from MongoDB
        mongodb_novels = self.mongodb_db.get_collection("novels")
        cursor = mongodb_novels.find({})
        old_novels = await cursor.to_list(length=None)
        
        migrated_count = 0
        async with AsyncSessionFactory() as db_session:
            for old_novel in old_novels:
                # Find corresponding user
                user = await self.get_user_by_username(db_session, old_novel.get('user'))
                if not user:
                    print(f"Skipping novel {old_novel.get('name')} - user not found")
                    continue
                
                # Create new novel
                new_novel = Novel(
                    title=old_novel.get('name', ''),
                    author=old_novel.get('author', ''),
                    description=old_novel.get('description', ''),
                    cover_image_url=old_novel.get('img', ''),
                    source_url=old_novel.get('novel_url', ''),
                    source_site=old_novel.get('origin', ''),
                    latest_chapter=old_novel.get('last_chapter', ''),
                    latest_chapter_url=old_novel.get('last_chapter_url', ''),
                    user_id=user.id  # Link to user
                )
                
                db_session.add(new_novel)
                try:
                    await db_session.commit()
                    await db_session.refresh(new_novel)
                    migrated_count += 1
                    print(f"Migrated novel: {old_novel.get('name')}")
                except Exception as e:
                    print(f"Error migrating novel {old_novel.get('name')}: {e}")
                    await db_session.rollback()
        
        print(f"Novel migration completed. Total migrated: {migrated_count}")

    async def run_migration(self):
        """
        Run the full migration process
        """
        print("Starting data migration from MongoDB to PostgreSQL...")
        
        await self.migrate_users()
        await self.migrate_novels()
        
        print("Data migration completed!")

    def close(self):
        """
        Close database connections
        """
        self.mongodb_client.close()


async def main():
    # These would come from environment variables in production
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    postgresql_uri = os.getenv("POSTGRESQL_URI", "postgresql+asyncpg://user:password@localhost/dbname")
    
    migrator = DataMigration(mongodb_uri, postgresql_uri)
    
    try:
        await migrator.run_migration()
    finally:
        migrator.close()


if __name__ == "__main__":
    asyncio.run(main())