# =============================================================================
# CASS - Copilot Instructions
# =============================================================================

## Project Overview
CASS (Conversational AI SQL System) is a text-to-SQL AI assistant using:
- **LLM**: Ollama with sqlcoder:7b model (local, free)
- **Backend**: Python + FastAPI
- **Frontend**: HTML/CSS/JS + Tailwind CSS
- **Database**: PostgreSQL
- **Deployment**: Vercel (frontend) + Railway (backend)

## Architecture
```
User Input → Frontend → SSE API → Agent → Ollama LLM → SQL Tool → PostgreSQL
                                    ↓
                              Streaming Response → Data Table / Chart / Answer
```

## Code Style
- **Python**: Black formatter, Ruff linter, type hints required
- **JavaScript**: Prettier formatter, ESLint, ES6+
- **SQL**: Uppercase keywords, lowercase identifiers

## Key Patterns
1. All LLM calls should support streaming
2. Tools must validate SQL before execution (no DROP, DELETE without WHERE)
3. Use async/await throughout backend
4. SSE events follow the format: `{ "type": "...", "content": "..." }`

## Team Structure
- **Person A**: Backend (Python, FastAPI, Agent, Ollama integration)
- **Person B**: Frontend (UI/UX, JavaScript, Tailwind, Vercel)
- **Person C**: Database (PostgreSQL, schema, DevOps, Railway)
