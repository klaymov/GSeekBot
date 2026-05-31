import aiohttp


class RapidAPIClient:
    """Client for RapidAPI Google Search."""

    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        self.api_key = api_key
        self.session = session
        self.base_url = "https://google-search143.p.rapidapi.com/api/v1/search"
        self.host = "google-search143.p.rapidapi.com"

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.host,
            "Content-Type": "application/json",
        }
        params = {"q": query, "limit": str(limit)}

        async with self.session.get(self.base_url, headers=headers, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            if data.get("ok"):
                return data.get("results", [])
            return []
