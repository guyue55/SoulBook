import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import httpx
from bs4 import BeautifulSoup


class BaseCrawler(ABC):
    """
    Base crawler class defining the interface for all crawlers
    """

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.client = httpx.AsyncClient(headers=self.headers, timeout=10.0)

    async def fetch(self, url: str) -> Optional[str]:
        """
        Fetch content from URL with retry mechanism
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return response.text
            except httpx.RequestError as e:
                print(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"All attempts failed for {url}")
                    return None
            except httpx.HTTPStatusError as e:
                print(f"HTTP error {e.response.status_code} for {url}")
                return None

    async def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content with BeautifulSoup
        """
        return BeautifulSoup(html, 'lxml')

    @abstractmethod
    async def search_novels(self, keyword: str) -> List[Dict[str, str]]:
        """
        Abstract method to search for novels by keyword
        """
        pass

    @abstractmethod
    async def get_novel_info(self, novel_url: str) -> Dict[str, str]:
        """
        Abstract method to get novel information from URL
        """
        pass

    @abstractmethod
    async def get_chapters(self, novel_url: str) -> List[Dict[str, str]]:
        """
        Abstract method to get chapters list from novel URL
        """
        pass

    @abstractmethod
    async def get_chapter_content(self, chapter_url: str) -> str:
        """
        Abstract method to get chapter content from URL
        """
        pass

    async def close(self):
        """
        Close the HTTP client
        """
        await self.client.aclose()