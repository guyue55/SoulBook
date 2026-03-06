from typing import Dict, List
from .base import BaseCrawler


class ZonghengCrawler(BaseCrawler):
    """
    Zongheng crawler implementation
    """

    def __init__(self):
        super().__init__(
            base_url="https://www.zongheng.com",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://www.zongheng.com/"
            }
        )

    async def search_novels(self, keyword: str) -> List[Dict[str, str]]:
        """
        Search novels on Zongheng by keyword
        """
        search_url = f"https://search.zongheng.com/s?keyword={keyword}"
        html = await self.fetch(search_url)
        
        if not html:
            return []

        soup = await self.parse_html(html)
        results = []

        # Find search result items (this selector may need adjustment based on actual site structure)
        items = soup.select('.se-result-item')
        
        for item in items[:10]:  # Limit to first 10 results
            try:
                title_elem = item.select_one('.bookinfo-name a')
                author_elem = item.select_one('.author')
                desc_elem = item.select_one('.book-dec')
                
                if title_elem and author_elem:
                    novel_info = {
                        'title': title_elem.get_text(strip=True),
                        'author': author_elem.get_text(strip=True),
                        'description': desc_elem.get_text(strip=True) if desc_elem else '',
                        'source_url': title_elem.get('href'),
                        'source_site': 'zongheng',
                        'cover_image_url': ''  # May extract if available
                    }
                    results.append(novel_info)
            except Exception as e:
                print(f"Error parsing search result: {e}")
                continue
        
        return results

    async def get_novel_info(self, novel_url: str) -> Dict[str, str]:
        """
        Get detailed novel information from Zongheng
        """
        html = await self.fetch(novel_url)
        
        if not html:
            return {}

        soup = await self.parse_html(html)
        
        try:
            # Extract novel details (selectors may need adjustment)
            title = soup.select_one('.book-meta h1')
            author = soup.select_one('.book-meta .au-name')
            desc = soup.select_one('.book-dec')
            cover = soup.select_one('.book-img img')
            
            novel_info = {
                'title': title.get_text(strip=True) if title else '',
                'author': author.get_text(strip=True) if author else '',
                'description': desc.get_text(strip=True) if desc else '',
                'cover_image_url': cover.get('src') if cover else '',
                'source_url': novel_url,
                'source_site': 'zongheng'
            }
            
            return novel_info
        except Exception as e:
            print(f"Error parsing novel info: {e}")
            return {}

    async def get_chapters(self, novel_url: str) -> List[Dict[str, str]]:
        """
        Get chapter list for a novel
        """
        # Modify URL to go to chapter list page
        chapter_url = novel_url.replace('.html', '/mulu.html')
        html = await self.fetch(chapter_url)
        
        if not html:
            return []

        soup = await self.parse_html(html)
        chapters = []
        
        # Find chapter list (selectors may need adjustment)
        chapter_items = soup.select('.volume-list .chapter-item a')
        
        for item in chapter_items:
            try:
                chapter_info = {
                    'title': item.get_text(strip=True),
                    'url': item.get('href')
                }
                chapters.append(chapter_info)
            except Exception as e:
                print(f"Error parsing chapter: {e}")
                continue
        
        return chapters

    async def get_chapter_content(self, chapter_url: str) -> str:
        """
        Get content of a specific chapter
        """
        html = await self.fetch(chapter_url)
        
        if not html:
            return ""

        soup = await self.parse_html(html)
        
        # Find chapter content (selector may need adjustment)
        content_div = soup.select_one('#chapterContent')
        if content_div:
            return content_div.get_text(strip=True)
        
        # Alternative selector
        content_div = soup.select_one('.reader-box .content')
        if content_div:
            return content_div.get_text(strip=True)
        
        return ""