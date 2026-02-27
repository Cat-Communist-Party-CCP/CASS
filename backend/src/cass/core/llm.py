from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import AsyncIterator


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class LlmMessage:
    role: Role
    content: str

@dataclass
class LlmResponse:
    content: str
    model: str
    tokens_used: int = 0


class LlmProvider(ABC):
    """
    Abstract base class for LLM providers.
    Both Ollama and OpenRouter will implement this interface.
    """

    @abstractmethod
    async def chat(self, messages: list[LlmMessage]) -> LlmResponse:
        """Send messages to the LLM and get a response."""
        pass

    @abstractmethod
    async def chat_stream(self, messages: list[LlmMessage]) -> AsyncIterator[str]:
        """Send messages and stream the response token by token."""
        pass
