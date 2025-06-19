import aiohttp
import asyncio
from bs4 import BeautifulSoup
from loguru import logger
from duckduckgo_search import DDGS


async def ddg_definitions(
    query: str,
    max_results: int = 10,
    pause_between: float = 1.0,
    retries: int = 3,
    retry_pause: float = 2.0
) -> tuple[str, str]:
    await asyncio.sleep(pause_between)
    attempt = 0
    results = []

    while attempt < retries:
        try:
            with DDGS() as ddgs:
                results = ddgs.text(
                    keywords=query,
                    max_results=max_results
                )
                return results
            break
        except Exception:
            attempt += 1
            if attempt >= retries:
                return None
            await asyncio.sleep(retry_pause)
    return None


async def ddg_html_search(query: str, max_results: int = 10) -> list[dict]:
    """
    Повертає list[dict] виду:
    [{'title': ..., 'url': ..., 'snippet': ...}, …]
    """
    try:
        url = "https://duckduckgo.com/html/"
        params = {"q": query}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                resp.raise_for_status()
                html = await resp.text()

        soup = BeautifulSoup(html, "html.parser")
        results = []

        for result in soup.select("div.result")[:max_results]:
            a_title = result.select_one("a.result__a")
            title = a_title.get_text(strip=True) if a_title else ""
            url = a_title["href"] if a_title and a_title.has_attr("href") else ""

            snippet_tag = (
                result.select_one("a.result__snippet") or  
                result.select_one("div.result__snippet") or      
                result.select_one(".result__body .snippet") or
                result.select_one(".result__snippet")       
            )
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

            results.append({
                "title": title,
                "href": 'https:'+url,
                "body": snippet
            })

        return results
    except Exception as e:
        logger.error(f"Error during DuckDuckGo HTML search: {e}")
        return None
    

async def get(text: str) -> str:
    result = await ddg_html_search(text)
    if result is None:
        result = await ddg_definitions(text)
        
    return result or None