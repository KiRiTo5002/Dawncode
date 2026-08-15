from typing import Any

from openai import AsyncOpenAI

from src.utils.config import API_KEY, BASE_URL, MODEL


class LLMClient:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
        )

    async def close(self):
        await self.client.close()

    async def chat_completion(
        self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]
    ):
        response = await self.client.chat.completions.create(
            model=MODEL,  # type: ignore
            messages=messages,  # type: ignore
            stream=False,
            tools=tools,  # type: ignore
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": True,
                },
                "reasoning_budget": 4096,
            },
        )

        return response.choices[0].message

    async def chat_completion_stream(
        self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]
    ):
        response = await self.client.chat.completions.create(
            model=MODEL,  # type: ignore
            messages=messages,  # type: ignore
            stream=True,
            tools=tools,  # type: ignore
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": False,
                },
                "reasoning_budget": 4096,
            },
        )

        return response
