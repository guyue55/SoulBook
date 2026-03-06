from typing import Dict, Any
import asyncio
import logging
from datetime import datetime


class CrawlerMiddleware:
    """
    Middleware for crawler operations
    Handles rate limiting, logging, and error handling
    """
    
    def __init__(self, rate_limit: int = 10, time_window: int = 60):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.requests = []
        self.logger = logging.getLogger(__name__)

    def _clean_old_requests(self):
        """
        Remove requests older than the time window
        """
        now = datetime.now()
        self.requests = [
            req_time for req_time in self.requests
            if (now - req_time).seconds < self.time_window
        ]

    async def check_rate_limit(self) -> bool:
        """
        Check if the rate limit is exceeded
        """
        self._clean_old_requests()
        
        if len(self.requests) >= self.rate_limit:
            return False
            
        self.requests.append(datetime.now())
        return True

    async def wait_if_needed(self):
        """
        Wait if rate limit would be exceeded
        """
        if not await self.check_rate_limit():
            self.logger.warning("Rate limit reached, waiting...")
            await asyncio.sleep(1)
            await self.wait_if_needed()  # Recursive call to check again

    async def log_request(self, url: str, status: str, duration: float):
        """
        Log request details
        """
        self.logger.info(f"CRAWLER REQUEST - URL: {url}, STATUS: {status}, DURATION: {duration:.2f}s")

    async def handle_error(self, url: str, error: Exception) -> Dict[str, Any]:
        """
        Handle errors during crawling
        """
        self.logger.error(f"CRAWLER ERROR - URL: {url}, ERROR: {str(error)}")
        return {
            "error": str(error),
            "url": url,
            "timestamp": datetime.now().isoformat()
        }

    async def process_response(self, url: str, response: str, duration: float):
        """
        Process successful response
        """
        await self.log_request(url, "SUCCESS", duration)
        return response