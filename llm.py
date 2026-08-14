from typing import Any

from openai import AsyncOpenAI

from config import API_KEY, BASE_URL, MODEL


class LLMClient:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
        )

    async def chat_completion(
        self,
        messages: list[dict[str, Any]],
    ):
        response = await self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=False,
        )

        return response.choices[0].message.content
