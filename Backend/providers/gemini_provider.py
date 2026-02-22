import json

from google import genai
from google.genai import types

from .base import LLMProvider


class GeminiProvider(LLMProvider):

    async def analyze(self, content: str, system_prompt: str) -> dict:
        client = genai.Client(api_key=self.api_key)
        response = await client.aio.models.generate_content(
            model=self.model,
            contents=content,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        return json.loads(response.text)
