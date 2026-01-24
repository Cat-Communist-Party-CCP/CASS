# CASS Internal Team Guide

> ⚠️ **INTERNAL DOCUMENT** - This guide is for team members only.

---

## 👥 Team Structure & Responsibilities

### 🔵 Person A: Backend Developer
**Focus:** Python, FastAPI, LLM Integration

| Week | Tasks |
|------|-------|
| 1 | Set up project structure, create core abstractions (`User`, `LlmMessage`, `Tool`) |
| 2 | Implement `OllamaService`, create `RunSqlTool`, `SchemaLookupTool` |
| 3 | Build `Agent` class with tool execution loop, implement streaming |
| 4 | Create FastAPI routes, SSE endpoints, error handling |
| 5 | Add fallback model support, optimize performance, write tests |

**Key Files to Create:**
```
backend/src/cass/core/agent.py
backend/src/cass/integrations/llm/ollama.py
backend/src/cass/server/routes.py
```

---

### 🟢 Person B: Frontend Developer
**Focus:** UI/UX, JavaScript, Tailwind CSS

| Week | Tasks |
|------|-------|
| 1 | Set up frontend project, design UI mockups, create base layout |
| 2 | Build chat components (messages, input box), implement SSE client |
| 3 | Create SQL block with syntax highlighting, data table component |
| 4 | Add chart visualizations, conversation history, dark/light theme |
| 5 | Responsive design, animations, Vercel deployment, polish |

**Key Files to Create:**
```
frontend/src/components/ChatContainer.js
frontend/src/components/DataTable.js
frontend/src/utils/sse.js
```

---

### 🟠 Person C: Database & DevOps
**Focus:** PostgreSQL, Docker, Integration

| Week | Tasks |
|------|-------|
| 1 | Set up PostgreSQL, design sample schema, create seed data |
| 2 | Create `PostgresRunner` class, connection pooling, schema introspection |
| 3 | Docker compose setup, environment configuration |
| 4 | Integration testing, API documentation, CI/CD pipeline |
| 5 | Backend deployment (Railway/Render), monitoring, final testing |

**Key Files to Create:**
```
backend/src/cass/integrations/database/postgres.py
database/schema.sql
docker-compose.yml
```

---

## 📁 Project Structure

```
CASS/
├── 📂 backend/                    # Python Backend (Person A)
│   ├── 📂 src/cass/
│   │   ├── 📂 core/               # Core abstractions
│   │   │   ├── agent.py           # Main AI agent orchestrator
│   │   │   ├── user.py            # User & auth management
│   │   │   ├── llm.py             # LLM service abstraction
│   │   │   ├── tool.py            # Tool base class
│   │   │   └── registry.py        # Tool registry
│   │   ├── 📂 integrations/       # External integrations
│   │   │   ├── 📂 llm/
│   │   │   │   ├── ollama.py      # Ollama integration
│   │   │   │   └── fallback.py    # Fallback model handler
│   │   │   └── 📂 database/
│   │   │       ├── base.py        # SQL runner base
│   │   │       └── postgres.py    # PostgreSQL runner
│   │   ├── 📂 tools/              # Built-in tools
│   │   │   ├── run_sql.py         # Execute SQL queries
│   │   │   └── schema.py          # Schema introspection
│   │   └── 📂 server/             # API layer
│   │       ├── app.py             # FastAPI application
│   │       ├── routes.py          # API endpoints
│   │       ├── chat_handler.py    # Chat logic
│   │       └── sse.py             # Server-Sent Events
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── 📂 frontend/                   # Web UI (Person B)
│   ├── 📂 public/
│   │   └── index.html
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── ChatContainer.js
│   │   │   ├── MessageList.js
│   │   │   ├── SqlBlock.js
│   │   │   ├── DataTable.js
│   │   │   └── Chart.js
│   │   ├── 📂 styles/
│   │   │   └── globals.css
│   │   ├── 📂 utils/
│   │   │   ├── sse.js
│   │   │   └── api.js
│   │   └── app.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── vercel.json
│
├── 📂 database/                   # Database (Person C)
│   ├── 📂 migrations/
│   ├── 📂 seeds/
│   ├── schema.sql
│   └── docker-compose.yml
│
├── 📂 docs/
│   ├── INTERNAL.md               # This file
│   ├── API.md
│   └── ARCHITECTURE.md
│
└── 📂 tests/
```

---

## 🚀 Development Setup

### Prerequisites

| Software | Version | Installation |
|----------|---------|--------------|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Ollama | Latest | [ollama.ai](https://ollama.ai) |
| PostgreSQL | 14+ | [postgresql.org](https://postgresql.org) |
| VS Code | Latest | [code.visualstudio.com](https://code.visualstudio.com) |
| Docker | Latest | [docker.com](https://docker.com) |

---

### Step 1: Clone & Setup

```powershell
git clone https://github.com/Cat-Communist-Party-CCP/CASS.git
cd CASS
```

---

### Step 2: Install Ollama & Models

```powershell
# Install Ollama (Windows)
winget install Ollama.Ollama

# Pull primary model (SQL-specialized)
ollama pull sqlcoder:7b

# Pull fallback model (smaller, faster)
ollama pull phi3:mini

# Verify installation
ollama list
```

---

### Step 3: Database Setup

```powershell
# Start PostgreSQL with Docker
docker-compose up -d

# Verify it's running
docker ps

# Access Adminer UI: http://localhost:8080
# Server: postgres | User: postgres | Password: casspass | Database: cassdb
```

---

### Step 4: Backend Setup (Person A)

```powershell
cd backend

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run backend
uvicorn src.cass.server.app:app --reload --host 0.0.0.0 --port 8000
```

---

### Step 5: Frontend Setup (Person B)

```powershell
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Frontend at: http://localhost:3000
```

---

## 🔄 VS Code Live Share Workflow

### Starting a Session

1. **Host (Person A)** starts Live Share:
   ```
   Ctrl+Shift+P → "Live Share: Start Collaboration Session"
   ```

2. **Share the link** with Person B and Person C

3. **Join Session:**
   ```
   Ctrl+Shift+P → "Live Share: Join Collaboration Session"
   ```

### Best Practices

- **Host:** Person A (has RTX 4050 for Ollama)
- **Share terminals** for running commands together
- **Follow Participant** for pair programming
- **Use co-editing** on same files when needed

---

## 📡 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message, receive SSE stream |
| GET | `/api/schema` | Get database schema |
| GET | `/api/history` | Get conversation history |
| GET | `/api/health` | Health check |

### SSE Event Types

```javascript
{ "type": "thinking", "content": "Analyzing your question..." }
{ "type": "sql", "content": "SELECT * FROM customers LIMIT 10;" }
{ "type": "executing", "content": "Running query..." }
{ "type": "data", "content": { "columns": [...], "rows": [...] } }
{ "type": "chart", "content": { "type": "bar", "data": {...} } }
{ "type": "answer", "content": "Here are the results..." }
{ "type": "error", "content": "Something went wrong" }
{ "type": "done" }
```

---

## 🦙 Model Fallback System

```
Primary: sqlcoder:7b (best quality)
    ↓ (if timeout/error)
Fallback: phi3:mini (faster, lower quality)
```

**Implementation:**
```python
class FallbackLlmService(LlmService):
    def __init__(self):
        self.primary = OllamaService(model="sqlcoder:7b")
        self.fallback = OllamaService(model="phi3:mini")
    
    async def complete(self, messages, **kwargs):
        try:
            return await asyncio.wait_for(
                self.primary.complete(messages, **kwargs),
                timeout=60.0
            )
        except (asyncio.TimeoutError, Exception):
            return await self.fallback.complete(messages, **kwargs)
```

---

## 🌐 Deployment

### Frontend → Vercel

1. Connect repo at [vercel.com/new](https://vercel.com/new)
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Add env var: `VITE_API_URL=https://your-backend.railway.app`

### Backend → Railway

1. Connect repo at [railway.app/new](https://railway.app/new)
2. Add PostgreSQL service
3. Set environment variables from `.env.example`

---

## 📋 Weekly Milestones

### Week 1: Foundation
- [ ] Project structure created
- [ ] Ollama installed and working
- [ ] PostgreSQL running with sample data
- [ ] Basic HTML layout done
- [ ] Live Share session established

### Week 2: Core Features
- [ ] `OllamaService` implemented
- [ ] `RunSqlTool` working
- [ ] Chat UI components built
- [ ] SSE connection established

### Week 3: Integration
- [ ] Agent executing tools
- [ ] Frontend receiving SSE events
- [ ] SQL results displaying in table
- [ ] End-to-end flow working

### Week 4: Polish
- [ ] Charts and visualizations
- [ ] Dark/light theme
- [ ] Error handling
- [ ] Conversation history

### Week 5: Deployment
- [ ] Frontend on Vercel
- [ ] Backend on Railway
- [ ] Documentation complete
- [ ] Demo ready

---

## 🔧 Git Workflow

```powershell
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add your feature description"

# Push to remote
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Branch Naming
- `feature/chat-ui` - New features
- `fix/sse-connection` - Bug fixes
- `docs/api-documentation` - Documentation

### Commit Messages
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructuring

---

## 🐛 Troubleshooting

### Ollama Not Responding
```powershell
ollama list
taskkill /IM ollama.exe /F
ollama serve
```

### PostgreSQL Connection Failed
```powershell
docker ps | findstr postgres
docker restart cass-postgres
```

### CORS Errors
Ensure backend has correct CORS origins in `.env`

### SSE Connection Drops
Add reconnection logic in frontend

---

## 📞 Team Communication

- **Daily Standups:** Share progress in team chat
- **Code Reviews:** All PRs need 1 approval
- **Questions:** Ask in team Discord/Slack

---

*Last updated: January 2026*
