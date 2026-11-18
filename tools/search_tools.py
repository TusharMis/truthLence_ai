"""
TruthLens AI - Search Tools
===========================
Executes live web search using Tavily API (dedicated research search)
with automatic fallback to DuckDuckGo (free, zero-API-key search).
Extracts clean search snippets, page titles, URLs, and evaluates domain trust.
"""

import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from config import settings

logger = logging.getLogger(__name__)

# Established credible news, academic, scientific, historical, and fact-checking domains
TRUSTED_DOMAINS = {
    "reuters.com", "apnews.com", "bbc.com", "bbc.co.uk", "nature.com",
    "science.org", "snopes.com", "politifact.com", "factcheck.org",
    "who.int", "cdc.gov", "nasa.gov", "nih.gov", "britannica.com",
    "theguardian.com", "nytimes.com", "wsj.com", "economist.com",
    "scientificamerican.com", "nationalgeographic.com", "pbs.org",
    "smithsonianmag.com", "webmd.com", "mayoclinic.org", "iwm.org.uk",
    "history.com", "healthline.com", "ncbi.nlm.nih.gov", "hopkinsmedicine.org",
    "aao.org", "clevelandclinic.org", "sciencedirect.com"
}


def is_trusted_domain(url: str) -> bool:
    """Checks whether the given URL originates from a high-credibility domain."""
    try:
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        if domain.endswith(".gov") or domain.endswith(".edu"):
            return True
        return any(domain == td or domain.endswith("." + td) for td in TRUSTED_DOMAINS)
    except Exception:
        return False


def extract_domain(url: str) -> str:
    """Extracts clean root domain from a URL."""
    try:
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain or "unknown"
    except Exception:
        return "unknown"


class SearchEngine:
    """Unified search client supporting Tavily Search API with DuckDuckGo fallback."""

    def __init__(
        self,
        tavily_key: Optional[str] = None,
        max_results: Optional[int] = None
    ):
        self.tavily_key = tavily_key or settings.tavily_api_key
        self.max_results = max_results or settings.max_search_results

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Executes live web search for a given query string.
        Prioritizes Tavily API; falls back to DuckDuckGo if Tavily is unconfigured or fails.
        """
        limit = max_results or self.max_results
        
        # 1. Try Tavily Search API
        if self.tavily_key and "your_tavily_api_key" not in self.tavily_key.lower():
            try:
                from tavily import TavilyClient
                client = TavilyClient(api_key=self.tavily_key)
                response = client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=limit,
                    include_raw_content=False
                )
                raw_results = response.get("results", [])
                formatted = []
                for r in raw_results:
                    url = r.get("url", "").strip()
                    if not url:
                        continue
                    formatted.append({
                        "title": r.get("title", "Untitled Source").strip(),
                        "url": url,
                        "snippet": r.get("content", "").strip(),
                        "domain": extract_domain(url),
                        "is_trusted": is_trusted_domain(url),
                        "score": r.get("score", 0.0),
                    })
                if formatted:
                    logger.info(f"Tavily search retrieved {len(formatted)} results for: {query}")
                    return formatted
            except Exception as e:
                logger.warning(f"Tavily search failed ({type(e).__name__}), falling back to DuckDuckGo: {e}")

        # 2. Fallback to DuckDuckGo Search
        try:
            try:
                from ddgs import DDGS
            except ImportError:
                from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(query, max_results=limit))
                formatted = []
                for r in ddg_results:
                    url = r.get("href", "").strip()
                    if not url:
                        continue
                    formatted.append({
                        "title": r.get("title", "Untitled Source").strip(),
                        "url": url,
                        "snippet": r.get("body", "").strip(),
                        "domain": extract_domain(url),
                        "is_trusted": is_trusted_domain(url),
                        "score": 0.5,
                    })
                logger.info(f"DuckDuckGo search retrieved {len(formatted)} results for: {query}")
                return formatted
        except Exception as e:
            logger.error(f"DuckDuckGo fallback search also failed: {e}")
            return []
