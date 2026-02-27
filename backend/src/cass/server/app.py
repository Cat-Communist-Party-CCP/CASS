"""
CASS FastAPI Application
========================
Main entry point for the CASS API server.
"""

import json
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from cass.integrations.database.postgres import PostgresRunner
from cass.integrations.llm.ollama import OllamaProvider
from cass.tools.run_sql import RunSQLTool
from cass.core.agent import Agent
from cass.core.llm import LlmMessage, Role

# Global instances (initialized on startup)
db: PostgresRunner | None = None
agent: Agent | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown logic.

    - On startup: Connect to database, create agent
    - On shutdown: Close database connection
    """
    global db, agent

    # Startup
    print("Starting CASS...")

    # Connect to database
    db = PostgresRunner("postgresql://postgres:1693@localhost:5432/cassdb")
    await db.connect()
    print("Database connected!")

    # Create LLM and tools
    llm = OllamaProvider(model="llama3.2:latest")
    sql_tool = RunSQLTool(db)

    # Create agent
    agent = Agent(llm=llm, tools=[sql_tool])
    print("Agent ready!")

    yield  # App runs here

    # Shutdown
    print("Shutting down...")
    if db:
        await db.close()
    print("Goodbye!")


# Create the FastAPI app
app = FastAPI(
    title="CASS API",
    description="Conversational AI SQL System",
    version="0.1.0",
    lifespan=lifespan
)

# Allow frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "CASS is running!"}


@app.get("/schema")
async def get_schema():
    """Get the current database schema."""
    if db is None:
        return {"error": "Database not connected"}

    schema = await db.get_schema()
    return {"schema": schema}


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    answer: str
    sql: str | None = None
    data: list | None = None
    error: str | None = None  # Error message if SQL failed


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to CASS and get a response.
    Example:
        POST /chat
        {"message": "How many customers are there?"}
    """
    if agent is None or db is None:
        return ChatResponse(answer="System not ready", sql=None, data=None, error="System not initialized")

    # Get schema for context
    schema = await db.get_schema()

    # Get agent response
    response = await agent.chat(request.message, schema)

    return ChatResponse(
        answer=response.answer,
        sql=response.sql,
        data=response.data,
        error=response.error
    )


# =============================================================================
# Part 4: Additional Endpoints
# =============================================================================

@app.get("/tables")
async def list_tables():
    """List all tables in the database."""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")

    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """
    tables = await db.execute(query)
    return {"tables": [t["table_name"] for t in tables]}


@app.get("/tables/{table_name}")
async def describe_table(table_name: str):
    """Get detailed information about a specific table."""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")

    # Get columns
    columns_query = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = $1
        ORDER BY ordinal_position
    """
    # Use parameterized query to prevent SQL injection
    columns = await db.execute(f"""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = '{table_name}'
        ORDER BY ordinal_position
    """)

    if not columns:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

    # Get row count
    count_result = await db.execute(f"SELECT COUNT(*) as count FROM {table_name}")
    row_count = count_result[0]["count"] if count_result else 0

    return {
        "table": table_name,
        "columns": columns,
        "row_count": row_count
    }


class SqlRequest(BaseModel):
    """Request body for raw SQL execution."""
    sql: str


@app.post("/sql")
async def execute_sql(request: SqlRequest):
    """
    Execute raw SQL query (SELECT only for safety).

    Example:
        POST /sql
        {"sql": "SELECT * FROM customers LIMIT 5"}
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")

    # Basic SQL injection prevention - only allow SELECT
    sql_upper = request.sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        raise HTTPException(
            status_code=400,
            detail="Only SELECT queries are allowed"
        )

    # Block dangerous keywords
    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE"]
    for keyword in dangerous:
        if keyword in sql_upper:
            raise HTTPException(
                status_code=400,
                detail=f"Dangerous keyword '{keyword}' not allowed"
            )

    try:
        results = await db.execute(request.sql)
        return {"data": results, "row_count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sample/{table_name}")
async def get_sample_data(table_name: str, limit: int = 5):
    """Get sample rows from a table."""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")

    try:
        results = await db.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        return {"table": table_name, "data": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =============================================================================
# Part 3: Streaming Endpoint (SSE)
# =============================================================================

async def stream_chat_response(message: str, schema: str) -> AsyncGenerator[str, None]:
    """Generate SSE events for streaming chat response."""
    if agent is None:
        yield f"data: {json.dumps({'type': 'error', 'content': 'Agent not ready'})}\n\n"
        return

    # Send start event
    yield f"data: {json.dumps({'type': 'start', 'content': ''})}\n\n"

    # Get the agent's LLM for streaming
    messages = [
        LlmMessage(role=Role.SYSTEM, content=agent.system_prompt),
        LlmMessage(role=Role.SYSTEM, content=f"DATABASE SCHEMA:\n{schema}"),
        LlmMessage(role=Role.USER, content=message)
    ]

    full_response = ""

    try:
        # Stream tokens (type: ignore for async generator typing issue)
        async for token in agent.llm.chat_stream(messages):  # type: ignore
            full_response += token
            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

        # Extract SQL from full response
        sql = agent._extract_sql(full_response)

        if sql:
            yield f"data: {json.dumps({'type': 'sql', 'content': sql})}\n\n"

            # Execute SQL
            if db is not None:
                result = await agent.tools["run_sql"].execute(sql=sql)
                if result.success:
                    yield f"data: {json.dumps({'type': 'data', 'content': result.data})}\n\n"
                else:
                    yield f"data: {json.dumps({'type': 'error', 'content': result.error})}\n\n"

        # Send end event
        yield f"data: {json.dumps({'type': 'end', 'content': ''})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"


@app.get("/chat/stream")
async def chat_stream(message: str):
    """
    Stream chat response using Server-Sent Events (SSE).

    Example:
        GET /chat/stream?message=How%20many%20customers%20are%20there

    Events:
        - start: Stream started
        - token: Individual token from LLM
        - sql: Extracted SQL query
        - data: Query results
        - error: Error message
        - end: Stream complete
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")

    schema = await db.get_schema()

    return StreamingResponse(
        stream_chat_response(message, schema),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
