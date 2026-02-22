import json

import httpx

from .base import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(self, api_key: str | None, model: str, base_url: str = "http://localhost:11434"):
        super().__init__(api_key, model)
        self.base_url = base_url

    async def analyze(self, content: str, system_prompt: str) -> dict:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": content},
                    ],
                    "format": "json",
                    "stream": False,
                    "options": {"temperature": 0.2},
                },
            )
            response.raise_for_status()
            data = response.json()
            return json.loads(data["message"]["content"])
