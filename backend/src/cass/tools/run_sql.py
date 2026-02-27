from cass.core.tool import Tool, ToolResult
from cass.integrations.database.postgres import PostgresRunner


class RunSQLTool(Tool):
    """Tool for executing SQL queries on the database."""

    def __init__(self, db: PostgresRunner) -> None:
        self._db = db

    @property
    def name(self) -> str:
        return "run_sql"

    @property
    def description(self) -> str:
        return "Executes a SQL query against on the database and returns the results."

    async def execute(self, sql: str) -> ToolResult:
        try:
            results = await self._db.execute(sql)
            return ToolResult(success=True, data=results)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


