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
    error: str | None = None  # Added for error handling


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
        """Generate improved system prompt for accurate SQL generation."""
        return """You are CASS, an expert SQL assistant that converts natural language questions into accurate PostgreSQL queries.

RULES:
1. ONLY output a SQL query wrapped in ```sql code blocks
2. NO explanations, NO commentary - just the SQL
3. Use ONLY tables and columns that exist in the provided schema
4. Always use table aliases for clarity in JOINs
5. Use appropriate aggregations (COUNT, SUM, AVG) when asked about totals/averages
6. Limit results to 100 rows unless user specifies otherwise
7. For "top N" questions, use ORDER BY with LIMIT
8. Handle NULL values appropriately
9. Use ILIKE for case-insensitive text searches
10. Format dates using PostgreSQL date functions

COMMON PATTERNS:
- "how many" → SELECT COUNT(*)
- "total/sum" → SELECT SUM(column)
- "average" → SELECT AVG(column)
- "list all" → SELECT * FROM table LIMIT 100
- "top N by X" → ORDER BY X DESC LIMIT N
- "between dates" → WHERE date_col BETWEEN 'start' AND 'end'

IMPORTANT:
- Check the schema carefully before writing queries
- Use exact column names from the schema (case-sensitive)
- Join tables using foreign key relationships
- Always include a semicolon at the end

Example:
User: How many customers are in New York?
```sql
SELECT COUNT(*) AS customer_count
FROM customers
WHERE city ILIKE '%new york%';
```"""

    async def chat(self, user_message: str, schema: str) -> AgentResponse:
        """Process a user message and return a response."""
        messages = [
            LlmMessage(role=Role.SYSTEM, content=self.system_prompt),
            LlmMessage(role=Role.SYSTEM, content=f"DATABASE SCHEMA:\n{schema}"),
            LlmMessage(role=Role.USER, content=user_message)
        ]

        try:
            # Get LLM response
            response = await self.llm.chat(messages)
        except Exception as e:
            return AgentResponse(
                answer="Failed to get response from AI",
                sql=None,
                data=None,
                error=f"LLM Error: {str(e)}"
            )

        # Extract SQL if present
        sql = self._extract_sql(response.content)

        # Execute SQL if found
        data = None
        error = None

        if sql and "run_sql" in self.tools:
            result = await self.tools["run_sql"].execute(sql=sql)
            if result.success:
                data = result.data
            else:
                error = result.error
                # Try to fix the SQL with a retry
                fixed_response = await self._retry_with_error(
                    user_message, schema, sql, result.error
                )
                if fixed_response:
                    return fixed_response

        return AgentResponse(
            answer=response.content,
            sql=sql,
            data=data,
            error=error
        )

    async def _retry_with_error(
        self,
        user_message: str,
        schema: str,
        failed_sql: str,
        error: str
    ) -> AgentResponse | None:
        """Retry SQL generation with error feedback."""
        retry_messages = [
            LlmMessage(role=Role.SYSTEM, content=self.system_prompt),
            LlmMessage(role=Role.SYSTEM, content=f"DATABASE SCHEMA:\n{schema}"),
            LlmMessage(role=Role.USER, content=user_message),
            LlmMessage(role=Role.ASSISTANT, content=f"```sql\n{failed_sql}\n```"),
            LlmMessage(role=Role.USER, content=f"""That SQL query failed with error:
{error}

Please fix the SQL query. Remember to:
- Use ONLY columns that exist in the schema
- Check spelling and case of column names
- Ensure proper JOIN conditions

Provide the corrected SQL:""")
        ]

        try:
            response = await self.llm.chat(retry_messages)
            sql = self._extract_sql(response.content)

            if sql and "run_sql" in self.tools:
                result = await self.tools["run_sql"].execute(sql=sql)
                if result.success:
                    return AgentResponse(
                        answer=response.content,
                        sql=sql,
                        data=result.data,
                        error=None
                    )
        except Exception:
            pass

        return None

    def _extract_sql(self, content: str) -> str | None:
        """Extract SQL from markdown code blocks."""
        pattern = r"```sql\s*(.*?)\s*```"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(1).strip()
        return None

