from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Soulbook API"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External APIs
    BAIDU_SEARCH_URL: str = "http://www.baidu.com/s"
    BING_SEARCH_URL: str = "https://www.bing.com/search"
    SO_SEARCH_URL: str = "https://www.so.com/s"
    
    # Crawling settings
    USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
    REQUEST_TIMEOUT: int = 10
    
    # Application settings
    DEBUG: bool = True
    TIMEZONE: str = "Asia/Shanghai"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()