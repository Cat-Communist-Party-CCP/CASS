import re
from dataclasses import dataclass
from typing import Any

from cass.core.llm import LlmProvider, LlmMessage, Role
from cass.core.tool import Tool, ToolResult


@dataclass
class AgentResponse:
    """Response from the agent."""
    answer: str
    sql: str | None = None
    data: Any = None


class Agent:
    """AI Agent that combines LLM and Tools to answer questions."""

    def __init__(
        self,
        llm: LlmProvider,
        tools: list[Tool],
        system_prompt: str | None = None
    ) -> None:
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.system_prompt = system_prompt or self._default_system_prompt()

    def _default_system_prompt(self) -> str:
        """Generate default system prompt with tool descriptions."""
        tool_descriptions = "\n".join(
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        )

        return f"""You are CASS, a helpful SQL assistant.
You have access to these tools:
{tool_descriptions}

When user asks a data question:
1. Generate the SQL query
2. Respond with ONLY the SQL, wrapped in ```sql code blocks
3. Do not explain, just give the SQL

Example:
User: How many customers are there?
You: ```sql
SELECT COUNT(*) FROM customers
```"""

    async def chat(self, user_message: str, schema: str) -> AgentResponse:
        """Process a user message and return a response."""
        messages = [
            LlmMessage(role=Role.SYSTEM, content=self.system_prompt),
            LlmMessage(role=Role.SYSTEM, content=f"Database Schema:\n{schema}"),
            LlmMessage(role=Role.USER, content=user_message)
        ]

        # Get LLM response
        response = await self.llm.chat(messages)

        # Extract SQL if present
        sql = self._extract_sql(response.content)

        # Execute SQL if found
        data = None
        if sql and "run_sql" in self.tools:
            result = await self.tools["run_sql"].execute(sql=sql)
            if result.success:
                data = result.data

        return AgentResponse(
            answer=response.content,
            sql=sql,
            data=data
        )

    def _extract_sql(self, content: str) -> str | None:
        """Extract SQL from markdown code blocks."""
        pattern = r"```sql\s*(.*?)\s*```"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(1).strip()
        return None

