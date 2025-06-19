import asyncio
from duckduckgo_search import DDGS


async def ddg_definitions(
    query: str,
    max_results: int = 5,
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