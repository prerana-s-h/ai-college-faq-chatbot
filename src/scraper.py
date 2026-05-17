"""
Web scraper for college website content.
Uses BeautifulSoup4 to extract clean text from web pages.
"""

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict


class CollegeWebScraper:
    """Scrapes and cleans content from college website pages."""

    def __init__(self, headers: Dict = None):
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (compatible; CollegeFAQBot/1.0)"
        }
        self.scraped_data = []

    def scrape_page(self, url: str) -> Dict:
        """Scrape a single page and return cleaned text with metadata."""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted elements
            for tag in soup(["script", "style", "nav", "footer", "header",
                             "aside", "iframe", "noscript", "form"]):
                tag.decompose()

            # Remove elements with common ad/nav class names
            for cls in ["sidebar", "menu", "nav", "footer", "advertisement",
                        "cookie", "popup", "social-share", "breadcrumb"]:
                for el in soup.find_all(class_=lambda c: c and cls in str(c).lower()):
                    el.decompose()

            text = soup.get_text(separator="\n", strip=True)

            # Clean up excessive whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = "\n".join(lines)

            return {
                "url": url,
                "title": soup.title.string.strip() if soup.title and soup.title.string else url,
                "content": clean_text,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

        except Exception as e:
            print(f"[Scraper] Error scraping {url}: {e}")
            return {"url": url, "title": "", "content": "", "error": str(e)}

    def scrape_site(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """Scrape multiple pages with rate limiting."""
        results = []
        for i, url in enumerate(urls):
            print(f"[Scraper] ({i + 1}/{len(urls)}) Scraping: {url}")
            data = self.scrape_page(url)
            if data.get("content"):
                results.append(data)
            time.sleep(delay)  # Be polite
        self.scraped_data = results
        return results

    def save_scraped(self, output_dir: str) -> str:
        """Save scraped content to a JSON file."""
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "scraped_content.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        print(f"[Scraper] Saved {len(self.scraped_data)} pages to {filepath}")
        return filepath
