import json

from openai import AsyncOpenAI

from .base import LLMProvider


class OpenAIProvider(LLMProvider):

    async def analyze(self, content: str, system_prompt: str) -> dict:
        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content},
            ],
            temperature=0.2,
        )
        return json.loads(response.choices[0].message.content)
