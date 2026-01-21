# CASS - Conversational AI SQL System

<p align="center">
  <img src="docs/assets/cass-logo.png" alt="CASS Logo" width="200"/>
</p>

<p align="center">
  <strong>🤖 Ask questions in plain English, get SQL answers instantly</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#team-workflow">Team Workflow</a> •
  <a href="#deployment">Deployment</a>
</p>

---

## 📖 Overview

CASS (Conversational AI SQL System) is an open-source text-to-SQL AI assistant that converts natural language questions into SQL queries. Built with a local LLM (Ollama), it provides enterprise-grade features without API costs.

```
User: "Show me the top 5 customers who spent the most last month"
     ↓
CASS: Generates SQL → Executes → Returns results + visualization
```

---

## ✨ Features

- 🗣️ **Natural Language to SQL** - Ask questions in plain English
- 🦙 **Local LLM** - Powered by Ollama (no API costs!)
- 📊 **Rich Visualizations** - Tables, charts, and data insights
- ⚡ **Real-time Streaming** - See responses as they generate
- 🔒 **Secure** - Your data never leaves your infrastructure
- 🎨 **Modern UI** - Beautiful, responsive chat interface
- 🐘 **PostgreSQL** - Production-ready database support

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **LLM** | Ollama + `sqlcoder:7b` | SQL generation |
| **Backend** | Python + FastAPI | API server, SSE streaming |
| **Database** | PostgreSQL | Data storage |
| **Frontend** | HTML/CSS/JS + Tailwind | Chat interface |
| **Deployment** | Vercel (frontend) + Railway/Render (backend) | Hosting |
| **Collaboration** | VS Code Live Share | Real-time pair programming |

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
│   │   │   ├── ChatContainer.js   # Main chat wrapper
│   │   │   ├── MessageList.js     # Message display
│   │   │   ├── UserMessage.js     # User bubble
│   │   │   ├── AssistantMessage.js# AI response
│   │   │   ├── SqlBlock.js        # SQL code display
│   │   │   ├── DataTable.js       # Results table
│   │   │   ├── Chart.js           # Visualizations
│   │   │   └── InputBox.js        # User input
│   │   ├── 📂 styles/
│   │   │   └── globals.css
│   │   ├── 📂 utils/
│   │   │   ├── sse.js             # SSE connection
│   │   │   └── api.js             # API helpers
│   │   └── app.js                 # Main app
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
├── 📂 docs/                       # Documentation
│   ├── 📂 assets/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── CONTRIBUTING.md
│
├── 📂 tests/
├── docker-compose.yml             # Full stack local dev
├── .gitignore
└── README.md
```

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

## 🚀 Getting Started

### Prerequisites

| Software | Version | Installation |
|----------|---------|--------------|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Ollama | Latest | [ollama.ai](https://ollama.ai) |
| PostgreSQL | 14+ | [postgresql.org](https://postgresql.org) |
| VS Code | Latest | [code.visualstudio.com](https://code.visualstudio.com) |
| Git | Latest | [git-scm.com](https://git-scm.com) |

---

### Step 1: Clone Repository

```powershell
git clone https://github.com/your-org/CASS.git
cd CASS
```

---

### Step 2: Install Ollama & Model

```powershell
# Install Ollama (Windows)
winget install Ollama.Ollama

# Pull the SQL-specialized model
ollama pull sqlcoder:7b

# Pull fallback model (smaller, faster)
ollama pull phi3:mini

# Verify installation
ollama list
```

**Expected Output:**
```
NAME              SIZE
sqlcoder:7b       4.1 GB
phi3:mini         2.3 GB
```

---

### Step 3: Set Up PostgreSQL

#### Option A: Docker (Recommended)
```powershell
# Start PostgreSQL container
docker run --name cass-postgres -e POSTGRES_PASSWORD=casspass -e POSTGRES_DB=cassdb -p 5432:5432 -d postgres:14

# Verify it's running
docker ps
```

#### Option B: Local Installation
```powershell
# After installing PostgreSQL, create database
psql -U postgres -c "CREATE DATABASE cassdb;"
```

---

### Step 4: Backend Setup (Person A)

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings
notepad .env
```

**`.env` Configuration:**
```env
# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=sqlcoder:7b
OLLAMA_FALLBACK_MODEL=phi3:mini
OLLAMA_TIMEOUT=120

# PostgreSQL Settings
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cassdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=casspass

# Server Settings
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Feature Flags
ENABLE_STREAMING=true
ENABLE_FALLBACK=true
MAX_QUERY_ROWS=1000
```

**Run Backend:**
```powershell
# Start the server
uvicorn src.cass.server.app:app --reload --host 0.0.0.0 --port 8000

# Server running at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

---

### Step 5: Frontend Setup (Person B)

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend running at: http://localhost:3000
```

---

### Step 6: Database Setup (Person C)

```powershell
# Navigate to database folder
cd database

# Run migrations
psql -U postgres -d cassdb -f schema.sql

# Seed sample data
psql -U postgres -d cassdb -f seeds/sample_data.sql
```

**Sample Schema (`database/schema.sql`):**
```sql
-- Customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock INTEGER DEFAULT 0
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    total_amount DECIMAL(10, 2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
```

---

## 🔄 Development Workflow

### VS Code Live Share Setup

1. **Install Extension:**
   - Open VS Code
   - Go to Extensions (`Ctrl+Shift+X`)
   - Search "Live Share" and install

2. **Start Session (Host):**
   ```
   Ctrl+Shift+P → "Live Share: Start Collaboration Session"
   ```

3. **Join Session (Others):**
   - Click the shared link
   - Or: `Ctrl+Shift+P → "Live Share: Join Collaboration Session"`

4. **Best Practices:**
   - Host should be Person A (backend machine with Ollama)
   - Share terminals for running commands together
   - Use "Follow Participant" for pair programming

---

### Git Workflow

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

**Branch Naming:**
- `feature/chat-ui` - New features
- `fix/sse-connection` - Bug fixes
- `docs/api-documentation` - Documentation

**Commit Messages:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructuring

---

## 🌐 Deployment

### Frontend → Vercel

1. **Connect Repository:**
   ```
   https://vercel.com/new → Import Git Repository
   ```

2. **Configure Build:**
   - Framework: Other
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Environment Variables:**
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```

4. **Deploy:**
   - Push to `main` branch
   - Vercel auto-deploys

**`frontend/vercel.json`:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

---

### Backend → Railway

1. **Connect Repository:**
   ```
   https://railway.app/new → Deploy from GitHub
   ```

2. **Add PostgreSQL:**
   - Click "New" → "Database" → "PostgreSQL"

3. **Environment Variables:**
   ```
   POSTGRES_HOST=${{Postgres.PGHOST}}
   POSTGRES_PORT=${{Postgres.PGPORT}}
   POSTGRES_DB=${{Postgres.PGDATABASE}}
   POSTGRES_USER=${{Postgres.PGUSER}}
   POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
   OLLAMA_BASE_URL=http://your-ollama-server:11434
   ```

4. **Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY src/ ./src/

   EXPOSE 8000

   CMD ["uvicorn", "src.cass.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

---

### Ollama Server (For Production)

Since Ollama runs locally, for production you have options:

**Option 1: Self-hosted VM (Recommended)**
```powershell
# On a cloud VM with GPU (e.g., AWS g4dn.xlarge, GCP n1-standard-4 + T4)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull sqlcoder:7b

# Expose to network
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

**Option 2: Use Person A's Laptop as Server**
```powershell
# On Person A's machine with RTX 4050
$env:OLLAMA_HOST = "0.0.0.0:11434"
ollama serve

# Others connect via local network IP
# http://192.168.x.x:11434
```

---

## 🔧 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message, receive SSE stream |
| GET | `/api/schema` | Get database schema |
| GET | `/api/history` | Get conversation history |
| GET | `/api/health` | Health check |

### SSE Events

```javascript
// Event types streamed from /api/chat
{ "type": "thinking", "content": "Analyzing your question..." }
{ "type": "sql", "content": "SELECT * FROM customers LIMIT 10;" }
{ "type": "executing", "content": "Running query..." }
{ "type": "data", "content": { "columns": [...], "rows": [...] } }
{ "type": "chart", "content": { "type": "bar", "data": {...} } }
{ "type": "answer", "content": "Here are the results..." }
{ "type": "error", "content": "Something went wrong" }
{ "type": "done" }
```

### Example Request

```javascript
const eventSource = new EventSource('/api/chat?message=' + encodeURIComponent(userMessage));

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case 'sql':
      displaySqlBlock(data.content);
      break;
    case 'data':
      displayDataTable(data.content);
      break;
    case 'answer':
      displayAnswer(data.content);
      break;
    case 'done':
      eventSource.close();
      break;
  }
};
```

---

## 🦙 Model Fallback System

CASS automatically falls back to a smaller model if the primary model fails:

```
Primary: sqlcoder:7b (best quality)
    ↓ (if timeout/error)
Fallback: phi3:mini (faster, lower quality)
```

**Configuration:**
```python
# backend/src/cass/integrations/llm/fallback.py

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
        except (asyncio.TimeoutError, Exception) as e:
            logger.warning(f"Primary model failed: {e}, using fallback")
            return await self.fallback.complete(messages, **kwargs)
```

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

## 🧪 Testing

```powershell
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# Integration test
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all customers"}'
```

---

## 🐛 Troubleshooting

### Ollama Not Responding
```powershell
# Check if Ollama is running
ollama list

# Restart Ollama
taskkill /IM ollama.exe /F
ollama serve
```

### PostgreSQL Connection Failed
```powershell
# Check if PostgreSQL is running
docker ps | findstr postgres

# Restart container
docker restart cass-postgres
```

### CORS Errors
```python
# Ensure CORS is configured in backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### SSE Connection Drops
```javascript
// Add reconnection logic
eventSource.onerror = () => {
  eventSource.close();
  setTimeout(() => connectSSE(), 3000);
};
```

---

## 📚 Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Vercel Documentation](https://vercel.com/docs)
- [VS Code Live Share](https://visualstudio.microsoft.com/services/live-share/)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

| Role | Responsibilities |
|------|------------------|
| **Person A** | Backend, LLM Integration, Agent |
| **Person B** | Frontend, UI/UX, Vercel Deployment |
| **Person C** | Database, DevOps, Integration |

---

<p align="center">
  Built with ❤️ by the CASS Team
</p>
