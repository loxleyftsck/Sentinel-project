"""
SENTINEL - News Article Scraper
Scrape financial news articles about insider trading from Indonesian news sites

Usage:
    python scripts/data/scrape_news.py --source kontan --max-articles 100
    python scripts/data/scrape_news.py --source all --max-articles 500
"""

import argparse
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsScraper:
    """Base class for news scraping"""
    
    def __init__(self, output_dir: str = "data/raw/news"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Headers to avoid being blocked
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        
        self.articles = []
        
    def fetch_page(self, url: str, retries: int = 3) -> BeautifulSoup:
        """Fetch page with retry logic"""
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        logger.error(f"Failed to fetch {url} after {retries} attempts")
        return None
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        return " ".join(text.split()).strip()
    
    def save_articles(self, source: str):
        """Save scraped articles to CSV"""
        if not self.articles:
            logger.warning("No articles to save")
            return
        
        df = pd.DataFrame(self.articles)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{source}_articles_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"✅ Saved {len(self.articles)} articles to {filename}")
        
        return filename


class KontanScraper(NewsScraper):
    """Scraper for Kontan.co.id"""
    
    BASE_URL = "https://newsrelease.kontan.co.id"
    SEARCH_URL = "https://newsrelease.kontan.co.id/search"
    
    def scrape(self, keywords: List[str], max_articles: int = 100):
        """Scrape articles from Kontan"""
        logger.info(f"🔍 Scraping Kontan.co.id for keywords: {keywords}")
        
        for keyword in keywords:
            logger.info(f"Searching for: {keyword}")
            
            # Search page
            search_url = f"{self.SEARCH_URL}?q={keyword}"
            soup = self.fetch_page(search_url)
            
            if not soup:
                continue
            
            # Find article links (adjust selector based on actual site structure)
            article_links = soup.find_all('a', class_='article-link')  # Example selector
            
            for link in article_links[:max_articles]:
                if len(self.articles) >= max_articles:
                    break
                
                try:
                    article_url = urljoin(self.BASE_URL, link.get('href'))
                    article_data = self.scrape_article(article_url, keyword)
                    
                    if article_data:
                        self.articles.append(article_data)
                        logger.info(f"✅ Scraped: {article_data['title'][:50]}...")
                    
                    # Be polite - don't hammer the server
                    time.sleep(random.uniform(1, 3))
                
                except Exception as e:
                    logger.error(f"Error scraping article: {e}")
                    continue
        
        return self.articles
    
    def scrape_article(self, url: str, keyword: str) -> Dict:
        """Scrape individual article"""
        soup = self.fetch_page(url)
        
        if not soup:
            return None
        
        try:
            # Extract article data (adjust selectors based on actual site)
            title = soup.find('h1', class_='article-title')
            title = self.clean_text(title.get_text()) if title else ""
            
            content = soup.find('div', class_='article-content')
            content = self.clean_text(content.get_text()) if content else ""
            
            date = soup.find('time')
            date_str = date.get('datetime') if date else datetime.now().isoformat()
            
            return {
                'url': url,
                'title': title,
                'content': content,
                'date': date_str,
                'source': 'Kontan',
                'keyword': keyword,
                'scraped_at': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error parsing article {url}: {e}")
            return None


class CNBCScraper(NewsScraper):
    """Scraper for CNBC Indonesia"""
    
    BASE_URL = "https://www.cnbcindonesia.com"
    
    def scrape(self, keywords: List[str], max_articles: int = 100):
        """Scrape articles from CNBC Indonesia"""
        logger.info(f"🔍 Scraping CNBC Indonesia for keywords: {keywords}")
        
        # Similar implementation as KontanScraper
        # Adjust selectors based on CNBC Indonesia's structure
        
        logger.warning("CNBC scraper not fully implemented - requires site structure analysis")
        return []


class BisnisScraper(NewsScraper):
    """Scraper for Bisnis.com"""
    
    BASE_URL = "https://finansial.bisnis.com"
    
    def scrape(self, keywords: List[str], max_articles: int = 100):
        """Scrape articles from Bisnis.com"""
        logger.info(f"🔍 Scraping Bisnis.com for keywords: {keywords}")
        
        # Similar implementation
        # Adjust selectors based on Bisnis.com's structure
        
        logger.warning("Bisnis scraper not fully implemented - requires site structure analysis")
        return []


def main():
    parser = argparse.ArgumentParser(description='Scrape Indonesian financial news')
    parser.add_argument(
        '--source',
        choices=['kontan', 'cnbc', 'bisnis', 'all'],
        default='kontan',
        help='News source to scrape'
    )
    parser.add_argument(
        '--max-articles',
        type=int,
        default=100,
        help='Maximum articles to scrape per keyword'
    )
    parser.add_argument(
        '--keywords',
        nargs='+',
        default=['insider trading', 'transaksi afiliasi', 'orang dalam perusahaan'],
        help='Keywords to search for'
    )
    
    args = parser.parse_args()
    
    # Select scraper
    scrapers = {
        'kontan': KontanScraper,
        'cnbc': CNBCScraper,
        'bisnis': BisnisScraper,
    }
    
    if args.source == 'all':
        sources = ['kontan', 'cnbc', 'bisnis']
    else:
        sources = [args.source]
    
    # Scrape from selected sources
    for source in sources:
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting scraper: {source.upper()}")
        logger.info(f"{'='*60}")
        
        scraper = scrapers[source]()
        articles = scraper.scrape(args.keywords, args.max_articles)
        
        if articles:
            filename = scraper.save_articles(source)
            logger.info(f"✅ {source}: {len(articles)} articles saved to {filename}")
        else:
            logger.warning(f"⚠️  {source}: No articles scraped")
    
    logger.info("\n✅ Scraping complete!")


if __name__ == "__main__":
    main()
