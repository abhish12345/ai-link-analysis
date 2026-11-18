"""
WebsiteExtractor: fetches HTML from a URL and extracts clean text content
using BeautifulSoup. Strips scripts, styles, nav, footers, etc.
"""
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from app.config import settings


# Tags that carry no useful business content
REMOVE_TAGS = [
    "script", "style", "noscript", "iframe", "svg", "canvas",
    "nav", "footer", "header", "aside", "form", "button",
    "meta", "link", "input", "select", "option",
]


class WebsiteExtractor:
    """Fetches and cleans website HTML into LLM-ready text."""

    @staticmethod
    def fetch_html(url: str) -> str:
        """Fetch raw HTML with a browser-like user agent."""
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        with httpx.Client(
            timeout=settings.REQUEST_TIMEOUT,
            follow_redirects=True,
            headers=headers,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text

    @staticmethod
    def extract_content(html: str, url: str) -> dict:
        """
        Parse HTML and return a dict with:
          - title: page <title>
          - meta_description: <meta name="description">
          - headings: all h1-h3 text
          - main_text: cleaned body text (truncated)
          - domain: the website domain
        """
        soup = BeautifulSoup(html, "html.parser")

        # Remove noise tags
        for tag in soup(REMOVE_TAGS):
            tag.decompose()

        # Title
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Meta description
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta_desc = meta_tag.get("content", "")

        # Headings
        headings = []
        for h in soup.find_all(["h1", "h2", "h3"]):
            text = h.get_text(strip=True)
            if text:
                headings.append(text)

        # Main text — get all paragraph text + list items
        text_parts = []
        for p in soup.find_all(["p", "li", "span", "div"]):
            text = p.get_text(strip=True)
            if text and len(text) > 2:
                text_parts.append(text)

        main_text = " ".join(text_parts)

        # Clean up whitespace
        main_text = " ".join(main_text.split())

        # Truncate to max length
        if len(main_text) > settings.MAX_CONTENT_LENGTH:
            main_text = main_text[:settings.MAX_CONTENT_LENGTH] + "..."

        # Domain
        parsed = urlparse(url)
        domain = parsed.hostname or ""

        return {
            "title": title,
            "meta_description": meta_desc,
            "headings": headings[:20],
            "main_text": main_text,
            "domain": domain,
            "url": url,
        }

    @staticmethod
    def extract(url: str) -> dict:
        """
        Full pipeline: fetch HTML + extract content.
        Raises exceptions on failure — caller should handle.
        """
        html = WebsiteExtractor.fetch_html(url)
        return WebsiteExtractor.extract_content(html, url)
