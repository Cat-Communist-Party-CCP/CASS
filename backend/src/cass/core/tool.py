from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: str | None = None


class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the tool."""
        pass
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this tool does (for the LLM)."""
        pass
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with the given input and return the result.
        Args:
            **kwargs: Input parameters for the tool, defined by the tool itself.
        Returns:
            ToolResult: The result of executing the tool, including success status, data, and error"""
        pass

