import aiohttp


class OpenRouterClient:
    """Client for OpenRouter API."""

    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        self.api_key = api_key
        self.session = session
        self.base_url = "https://openrouter.ai/api/v1"

    async def ask(self, query: str) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Answer the user's question directly and concisely in the same language "
                        "the user used. Your response must not exceed 100 characters. "
                        "If you cannot provide a direct answer, respond with exactly 'False' "
                        "and nothing else."
                    )
                },
                {"role": "user", "content": query}
            ],
            "max_tokens": 50
        }

        async with self.session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]
