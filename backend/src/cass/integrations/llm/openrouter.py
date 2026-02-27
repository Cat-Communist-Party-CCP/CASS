import json
import httpx
from typing import AsyncIterator

from cass.core.llm import LlmProvider, LlmMessage, LlmResponse


class OpenRouterProvider(LlmProvider):
    """LLM provider using OpenRouter API for cloud models."""

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek/deepseek-chat",
        timeout: int = 120
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.base_url = "https://openrouter.ai/api/v1"

    def _format_messages(self, messages: list[LlmMessage]) -> list[dict]:
        """Convert LlmMessage objects to OpenRouter format."""
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]

    async def chat(self, messages: list[LlmMessage]) -> LlmResponse:
        """Send messages to OpenRouter and get a response."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json={
                    "model": self.model,
                    "messages": self._format_messages(messages),
                    "stream": False
                }
            )
            response.raise_for_status()
            data = response.json()

            return LlmResponse(
                content=data["choices"][0]["message"]["content"],
                model=self.model,
                tokens_used=data.get("usage", {}).get("total_tokens", 0)
            )

    async def chat_stream(self, messages: list[LlmMessage]) -> AsyncIterator[str]:
        """Stream response from OpenRouter token by token."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=headers,
                json={
                    "model": self.model,
                    "messages": self._format_messages(messages),
                    "stream": True
                }
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # Remove "data: " prefix
                        if data_str == "[DONE]":
                            break
                        data = json.loads(data_str)
                        if data["choices"][0].get("delta", {}).get("content"):
                            yield data["choices"][0]["delta"]["content"]
