# FastAPI Base Project

A modular FastAPI project template with JWT authentication, SQLAlchemy ORM, Alembic migrations, and LangGraph AI agents.

## Purpose

This project serves as a **production-ready template** for building AI agents with LangGraph and exposing them through FastAPI endpoints. It eliminates the need to configure authentication, database management, API routing, and agent infrastructure from scratch.

**Key Goals:**
- **Rapid Agent Development**: Start building LangGraph agents immediately without boilerplate setup
- **Production-Ready API**: Pre-configured FastAPI with JWT authentication, CORS, and comprehensive error handling
- **State Persistence**: Built-in PostgreSQL checkpointing for maintaining conversation history
- **Developer Experience**: Hot-reloading with `langgraph dev`, interactive API docs, and comprehensive testing tools
- **Scalability**: Modular architecture that scales from simple chatbots to complex multi-agent systems

Whether you're prototyping a conversational AI, building a production agent system, or learning LangGraph, this template provides everything you need to get started quickly.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy ORM** - Powerful database ORM with support for multiple databases
- **JWT Authentication** - Secure authentication using JSON Web Tokens with bcrypt password hashing
- **Rate Limiting** - Per-user rate limiting for chatbot endpoints (5 queries/24 hours configurable)
- **Alembic** - Database migration management
- **LangGraph Agents** - AI agents with state persistence using LangGraph
- **Modular Architecture** - Clean separation of concerns with routers, services, and models
- **Pydantic Schemas** - Request/response validation and serialization
- **CORS Support** - Cross-Origin Resource Sharing enabled
- **Base Models** - Pre-built User and Profile models with relationships
- **Usage Tracking** - Automatic logging of all chatbot queries with token usage statistics

## Project Structure

```
agent-base-project/
├── src/
│   ├── main.py              # Application entry point
│   ├── core/                # Core configuration and security
│   │   ├── config.py        # Settings and environment variables
│   │   ├── security.py      # JWT and password hashing utilities
│   │   └── constants.py     # Application constants
│   ├── db/                  # Database configuration
│   │   ├── database.py      # SQLAlchemy engine setup
│   │   ├── session.py       # Database session management
│   │   └── checkpoint.py    # LangGraph checkpoint configuration
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── base.py          # Declarative base
│   │   ├── user.py          # User model
│   │   └── profile.py       # Profile model
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py          # User schemas (Create, Update, Read)
│   │   ├── profile.py       # Profile schemas
│   │   ├── token.py         # Authentication token schemas
│   │   └── common.py        # Common/shared schemas
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py  # Authentication logic
│   │   ├── user_service.py  # User management logic
│   │   └── profile_service.py # Profile management logic
│   ├── routers/             # API endpoints
│   │   ├── auth.py          # Authentication routes
│   │   ├── chatbot.py       # Chatbot/Agent routes
│   │   ├── users.py         # User management routes
│   │   └── profiles.py      # Profile routes
│   └── dependencies.py      # Shared dependencies (auth, etc.)
├── agents/                  # LangGraph agents
│   └── basic/               # Basic chatbot agent
│       ├── agent.py         # Agent graph definition
│       ├── state.py         # Agent state schema
│       └── nodes/           # Agent nodes
│           └── chatbot/     # Chatbot node
│               ├── node.py  # Node implementation
│               └── prompt.py # System prompt
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── .env.example             # Environment variables template
├── langgraph.json           # LangGraph configuration
├── pyproject.toml           # Project configuration and dependencies (uv)
├── requirements.txt         # Python dependencies (alternative to pyproject.toml)
└── README.md               # This file
```

## Setup Instructions

> **🚀 New to this project?** Check out **[GETTING_STARTED.md](GETTING_STARTED.md)** for a complete beginner-friendly guide with troubleshooting tips!

Follow these steps to set up and run the project:

### Step 0: Clone the Repository

First, clone the repository to your local machine:

**Using HTTPS:**
```bash
git clone https://github.com/dinnovos/agent-base-project.git
cd agent-base-project
```

**Using SSH:**
```bash
git clone git@github.com:dinnovos/agent-base-project.git
cd agent-base-project
```

**Using GitHub CLI:**
```bash
gh repo clone dinnovos/agent-base-project
cd agent-base-project
```

> **Note:** If you're creating a new project based on this template, you can use GitHub's "Use this template" button or fork the repository instead of cloning it directly.

### Step 1: Install uv

First, install `uv` if you haven't already:

**On Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**On Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Create Virtual Environment and Install Dependencies

```bash
# Create virtual environment and install dependencies in one command
uv sync
```

This will:
- Create a `.venv` virtual environment automatically
- Install all dependencies from `pyproject.toml`
- Be much faster than traditional pip

**Alternative:** If you prefer using `requirements.txt`:
```bash
# Create virtual environment
uv venv

# Activate it (Windows)
.venv\Scripts\activate

# Activate it (Linux/Mac)
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### Step 3: Activate Virtual Environment (if not using uv sync)

**On Windows:**
```bash
.venv\Scripts\activate
```

**On Linux/Mac:**
```bash
source .venv/bin/activate
```

### Step 4: Configure Environment Variables

**On Windows:**
```bash
copy .env.example .env
```

**On Linux/Mac:**
```bash
cp .env.example .env
```

Then edit the `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=sqlite:///./app.db

# JWT Configuration
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Bcrypt Configuration
BCRYPT_ROUNDS=10

# Chatbot Rate Limiting
CHATBOT_QUERY_LIMIT=5
CHATBOT_QUERY_WINDOW_HOURS=24

# OpenAI Configuration (Required for LangGraph Agent)
OPENAI_API_KEY=sk-your-openai-api-key-here

# LangSmith Configuration (Optional - for tracing and monitoring)
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_xxx
```

**Generate a secure SECRET_KEY:**
```bash
# Using openssl
openssl rand -hex 32

# Or using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

**Important:** You need to set your OpenAI API key to use the chatbot agent. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

### Step 5: Initialize Database

Create the initial database migration:
```bash
alembic revision --autogenerate -m "initial migration"
```

Apply the migration to create tables:
```bash
alembic upgrade head
```

> **Note:** The application also has `Base.metadata.create_all(bind=engine)` in `src/main.py` which will create tables automatically if they don't exist. However, using Alembic migrations is recommended for production and better database version control.

### Step 6: Run the Application

#### Development (Windows)

**⚠️ Important for Windows Users**: Due to psycopg async driver requirements, you must use one of these methods:

**Option 1: Using the run script (Recommended)**
```bash
python run.py
```

**Option 2: Using uvicorn with loop parameter**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --loop asyncio
```

#### Development (Linux/macOS)

```bash
# Using the run script
python run.py

# Or using uvicorn directly
uvicorn src.main:app --reload
```

#### Production

**Railway/Docker (Linux containers)**
```bash
# No special configuration needed - works out of the box
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Windows Server**
```bash
# Use the --loop parameter
uvicorn src.main:app --host 0.0.0.0 --port 8000 --loop asyncio
```

**Linux/macOS Server**
```bash
# Standard command
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Or with Gunicorn for better performance
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The API will be available at:
- **URL**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

#### Why the difference?

- **Windows**: Uses `ProactorEventLoop` by default, but psycopg (async PostgreSQL driver) requires `SelectorEventLoop`
- **Linux/macOS**: Uses `SelectorEventLoop` by default, so no special configuration needed
- **Docker/Railway**: Runs Linux containers, so no special configuration needed

---

## Alternative Setup Methods

### Using Docker Compose

If you prefer using Docker:

```bash
docker-compose up
```

This will start both the application and a PostgreSQL database.

## API Endpoints

### Root

- **`GET /`** - Root endpoint, returns API information
  - No authentication required
  - Returns project name, status, and docs link

- **`GET /health`** - Health check endpoint
  - No authentication required
  - Returns health status

### Authentication (`/auth`)

- **`POST /auth/register`** - Register a new user
  - **Body**: `{ "username", "email", "password", "first_name"?, "last_name"? }`
  - **Returns**: User object (without password)
  - **Status**: 201 Created
  - Automatically creates a Profile for the user
  - Validates email format and password strength (min 8 chars)
  - Returns 400 if email or username already exists

- **`POST /auth/token`** - Login and get JWT access token
  - **Body**: Form data with `username` (email) and `password`
  - **Returns**: `{ "access_token", "token_type": "bearer" }`
  - **Status**: 200 OK
  - Returns 401 if credentials are invalid
  - Updates user's `last_login` timestamp
  - Token expires according to `ACCESS_TOKEN_EXPIRE_MINUTES` setting

### Users (`/users`)

🔒 All user endpoints require authentication (Bearer token)

- **`GET /users/me`** - Get current authenticated user information
  - **Returns**: Complete user object with all fields
  - **Status**: 200 OK

- **`GET /users/{id}`** - Get user by ID
  - **Returns**: User object
  - **Status**: 200 OK
  - **Permissions**: Users can only view their own profile unless they are staff/superuser
  - Returns 403 if insufficient permissions
  - Returns 404 if user not found

- **`PATCH /users/{id}`** - Update user information
  - **Body**: Any of `{ "username", "email", "password", "first_name", "last_name", "is_active" }`
  - **Returns**: Updated user object
  - **Status**: 200 OK
  - **Permissions**: Users can only update their own profile unless they are superuser
  - Regular users cannot modify `is_active` field
  - Password will be automatically hashed if provided
  - Returns 403 if insufficient permissions
  - Returns 404 if user not found

### Profiles (`/profiles`)

🔒 All profile endpoints require authentication (Bearer token)

- **`GET /profiles/me`** - Get current user's profile
  - **Returns**: Profile object with `time_zone`, `language`, `preferences`, timestamps
  - **Status**: 200 OK
  - Returns 404 if profile not found (shouldn't happen if created with user)

- **`PATCH /profiles/me`** - Update current user's profile
  - **Body**: Any of `{ "time_zone", "language", "preferences", "is_active" }`
  - **Returns**: Updated profile object
  - **Status**: 200 OK
  - `preferences` field can store JSON string for custom settings
  - Returns 404 if profile not found

### Chatbot (`/chatbot`)

🔒 All chatbot endpoints require authentication (Bearer token)

- **`POST /chatbot`** - Send a message to the chatbot agent
  - **Body**: `{ "message": "your message here" }`
  - **Returns**: String with the agent's response
  - **Status**: 200 OK
  - **Rate Limit**: 5 queries per 24 hours per user
  - Uses LangGraph agent with state persistence (thread_id: "1")
  - Maintains conversation history across requests
  - Returns HTTP 429 if rate limit exceeded

- **`POST /chatbot/stream`** - Send a message and receive streaming response
  - **Body**: `{ "message": "your message here" }`
  - **Returns**: Server-Sent Events (SSE) stream with agent's response chunks
  - **Status**: 200 OK
  - **Content-Type**: `text/event-stream`
  - **Rate Limit**: 5 queries per 24 hours per user
  - Uses LangGraph agent with state persistence (thread_id: "2")
  - Streams response in real-time as it's generated
  - Returns HTTP 429 if rate limit exceeded

- **`GET /chatbot/usage`** - Check current rate limit usage
  - **Returns**: `{ "used": int, "remaining": int, "limit": int, "window_hours": int, "can_query": bool }`
  - **Status**: 200 OK
  - Shows how many queries user has made in the current 24-hour window
  - Shows remaining queries before hitting the limit

## Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_staff": false,
  "is_superuser": false,
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": null
}
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepass123"
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Current User Info (Authenticated)

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. Update User Profile

```bash
curl -X PATCH "http://localhost:8000/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith"
  }'
```

### 5. Get Current User's Profile

```bash
curl -X GET "http://localhost:8000/profiles/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 6. Update Profile Settings

```bash
curl -X PATCH "http://localhost:8000/profiles/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "time_zone": "America/New_York",
    "language": "es",
    "preferences": "{\"theme\": \"dark\", \"notifications\": true}"
  }'
```

### 7. Chat with the Agent (Non-Streaming)

```bash
curl -X POST "http://localhost:8000/chatbot" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! What can you help me with?"
  }'
```

**Response:**
```
"Hello! I'm here to help you with a variety of tasks..."
```

### 8. Chat with the Agent (Streaming)

```bash
curl -X POST "http://localhost:8000/chatbot/stream" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me a short story"
  }'
```

**Response (Server-Sent Events):**
```
data: Once
data:  upon
data:  a
data:  time
data: ...
```

### 9. Check Chatbot Rate Limit Usage

```bash
curl -X GET "http://localhost:8000/chatbot/usage" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response (200 OK):**
```json
{
  "used": 3,
  "remaining": 2,
  "limit": 5,
  "window_hours": 24,
  "can_query": true
}
```

**When Rate Limit Exceeded (429 Too Many Requests):**
```json
{
  "detail": {
    "message": "Rate limit exceeded. You have used 5 of 5 queries in the last 24 hours.",
    "queries_used": 5,
    "queries_limit": 5,
    "window_hours": 24,
    "queries_remaining": 0
  }
}
```

## Rate Limiting

The chatbot endpoints implement a rate limiting mechanism to control API usage:

### Configuration

Rate limiting is configured via environment variables in `.env`:

```env
# Maximum number of queries per user
CHATBOT_QUERY_LIMIT=5

# Time window in hours
CHATBOT_QUERY_WINDOW_HOURS=24
```

### How It Works

- **Per-User Limiting**: Each authenticated user has their own quota
- **24-Hour Window**: The limit is based on a sliding 24-hour window
- **Unique Query Counting**: Queries are counted by unique `main_call_tid` values
- **Automatic Tracking**: Uses existing `UsageLog` table - no additional database tables needed

### Rate Limit Behavior

**When Within Limit:**
- Requests are processed normally
- Response includes standard HTTP 200 status

**When Limit Exceeded:**
- Request returns HTTP 429 (Too Many Requests)
- Includes detailed error message with usage information
- Includes `X-RateLimit-*` headers for client handling

### Checking Usage

Use the `/chatbot/usage` endpoint to check current usage:

```bash
curl -X GET "http://localhost:8000/chatbot/usage" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Returns:
```json
{
  "used": 3,
  "remaining": 2,
  "limit": 5,
  "window_hours": 24,
  "can_query": true
}
```

### Customizing Limits

To change rate limiting for different user types or scenarios:

```env
# Example: 10 queries per 12 hours
CHATBOT_QUERY_LIMIT=10
CHATBOT_QUERY_WINDOW_HOURS=12

# Example: Unlimited (development)
CHATBOT_QUERY_LIMIT=1000
CHATBOT_QUERY_WINDOW_HOURS=24
```

### Implementation Details

- **Service**: `check_chatbot_rate_limit()` in `src/services/usage_log_service.py`
- **Dependency**: `verify_chatbot_rate_limit()` in `src/dependencies.py`
- **Endpoints Protected**: `POST /chatbot`, `POST /chatbot/stream`
- **Endpoint for Checking**: `GET /chatbot/usage`

For more details, see `RATE_LIMITING_SETUP.md`.

---

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

## LangGraph Agent Testing

The project includes a basic chatbot agent built with LangGraph. You can test it in multiple ways:

### Option 1: Testing with LangGraph Studio (LangSmith)

LangGraph Studio provides a visual interface for testing and debugging your agents with full tracing capabilities.

#### Prerequisites

1. **Install LangGraph CLI** (if not already installed):
   ```bash
   uv pip install langgraph-cli
   ```

2. **Configure LangSmith** (optional but recommended for tracing):
   
   Get your API key from [LangSmith](https://smith.langchain.com/) and add to `.env`:
   ```env
   LANGSMITH_TRACING=true
   LANGSMITH_API_KEY=lsv2_your_api_key_here
   ```

3. **Set OpenAI API Key** in `.env`:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

#### Start LangGraph Dev Server

Run the following command in your project root:

```bash
langgraph dev
```

This will:
- Start the LangGraph development server
- Open LangGraph Studio in your browser (typically at `http://localhost:8123`)
- Enable hot-reloading for agent changes
- Provide visual debugging and tracing

#### Using LangGraph Studio

1. **Select the Agent**: Choose the `chatbot` graph from the dropdown
2. **Configure Thread**: Set a thread ID for conversation persistence
3. **Send Messages**: Type messages in the input box and see responses
4. **View State**: Inspect the agent's state at each step
5. **Trace Execution**: See detailed traces of LLM calls and node executions

#### LangGraph Configuration

The agent is configured in `langgraph.json`:
```json
{
  "dependencies": ["."],
  "graphs": {
    "chatbot": "agents/basic/agent.py:make_graph"
  },
  "env": ".env"
}
```

### Option 2: Testing via FastAPI Endpoints

You can test the agent through the FastAPI endpoints after starting the application.

#### Start the FastAPI Server

```bash
# Using the run script
python run.py

# Or using uvicorn directly
uvicorn src.main:app --reload
```

#### Test Non-Streaming Endpoint

**Using curl:**
```bash
# First, get an authentication token
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_email@example.com&password=your_password" \
  | jq -r '.access_token')

# Then chat with the agent
curl -X POST "http://localhost:8000/chatbot" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Can you help me?"
  }'
```

**Using Python:**
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/token",
    data={"username": "your_email@example.com", "password": "your_password"}
)
token = response.json()["access_token"]

# Chat with agent
response = requests.post(
    "http://localhost:8000/chatbot",
    headers={"Authorization": f"Bearer {token}"},
    json={"message": "Hello! Can you help me?"}
)
print(response.text)
```

**Using the provided `api.http` file:**

Open `api.http` in VS Code with the REST Client extension:

1. First, execute the login request to get a token
2. Copy the `access_token` from the response
3. Update the `@token` variable at the top of the file
4. Execute the chatbot requests

```http
### Chat (Non-Streaming)
POST {{baseUrl}}/chatbot HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
  "message": "Hello! What can you help me with?"
}

### Chat (Streaming)
POST {{baseUrl}}/chatbot/stream HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
  "message": "Tell me a short story"
}
```

#### Test Streaming Endpoint

**Using curl:**
```bash
curl -N -X POST "http://localhost:8000/chatbot/stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me a story"
  }'
```

**Using Python with SSE:**
```python
import requests
import json

# Login first (same as above)
response = requests.post(
    "http://localhost:8000/auth/token",
    data={"username": "your_email@example.com", "password": "your_password"}
)
token = response.json()["access_token"]

# Stream chat response
response = requests.post(
    "http://localhost:8000/chatbot/stream",
    headers={"Authorization": f"Bearer {token}"},
    json={"message": "Tell me a story"},
    stream=True
)

for line in response.iter_lines():
    if line:
        decoded_line = line.decode('utf-8')
        if decoded_line.startswith('data: '):
            content = decoded_line[6:]  # Remove 'data: ' prefix
            print(content, end='', flush=True)
```

### Option 3: Testing via Swagger UI

1. Start the FastAPI server: `python run.py`
2. Open http://localhost:8000/docs
3. Authenticate:
   - Click "Authorize" button
   - Login via `/auth/token` endpoint
   - Copy the access token
   - Enter `Bearer <token>` in the authorization dialog
4. Test the chatbot endpoints:
   - Expand `/chatbot` POST endpoint
   - Click "Try it out"
   - Enter your message in the request body
   - Click "Execute"

### Agent Architecture

The basic chatbot agent consists of:

- **State**: Defined in `agents/basic/state.py` - Manages conversation messages
- **Graph**: Defined in `agents/basic/agent.py` - Orchestrates the conversation flow
- **Nodes**: 
  - `chatbot` node in `agents/basic/nodes/chatbot/node.py` - Handles LLM interaction
- **Checkpoint**: PostgreSQL-based state persistence for conversation history
- **LLM**: Uses OpenAI's GPT-4o-mini model

### Conversation Persistence

The agent uses PostgreSQL checkpointing to maintain conversation history:

- **Thread ID**: Each conversation has a unique thread ID
- **State Persistence**: Messages are stored and retrieved across requests
- **Multiple Conversations**: Different thread IDs maintain separate conversations

Example with different threads:
```bash
# Conversation 1 (thread_id: "1" - used by /chatbot endpoint)
curl -X POST "http://localhost:8000/chatbot" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "My name is Alice"}'

curl -X POST "http://localhost:8000/chatbot" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my name?"}'
# Response: "Your name is Alice"

# Conversation 2 (thread_id: "2" - used by /chatbot/stream endpoint)
# This will be a separate conversation with no memory of "Alice"
```

### Customizing the Agent

To modify the agent behavior:

1. **Change the LLM model**: Edit `agents/basic/nodes/chatbot/node.py`
   ```python
   llm = init_chat_model("openai:gpt-4o", temperature=0.7)
   ```

2. **Modify the system prompt**: Edit `agents/basic/nodes/chatbot/prompt.py`

3. **Add new nodes**: Create new node files in `agents/basic/nodes/`

4. **Update the graph**: Modify `agents/basic/agent.py` to add edges and nodes

5. **Test changes**: Use `langgraph dev` for hot-reloading during development

## Architecture Principles

This template follows these key principles:

1. **Layered Architecture**: Clear separation between routers (HTTP), services (business logic), and models (data)
2. **No Business Logic in Routers**: All business logic resides in service layer
3. **Dependency Injection**: Database sessions and authentication via FastAPI's Depends
4. **Schema Separation**: Distinct Create, Update, and Read schemas for each model
5. **Bidirectional Relationships**: Models use SQLAlchemy relationships properly
6. **Security First**: Passwords hashed with bcrypt, JWT for stateless auth

## Extending the Template

### Adding a New Model

1. Create model in `src/models/new_model.py` (inherit from `Base`)
2. Create schemas in `src/schemas/new_model.py` (Create, Update, Read)
3. Create service in `src/services/new_model_service.py`
4. Create router in `src/routers/new_model.py`
5. Include router in `src/main.py`
6. Generate migration: `alembic revision --autogenerate -m "add new_model"`
7. Apply migration: `alembic upgrade head`

## Database Support

The template works with:

- **SQLite** (default, for development)
  ```env
  DATABASE_URL=sqlite:///./app.db
  ```

- **PostgreSQL** (recommended for production)
  ```env
  DATABASE_URL=postgresql://user:password@localhost:5432/dbname
  ```

- **MySQL**
  ```env
  DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname
  ```

Change `DATABASE_URL` in `.env` accordingly.

## Docker Support

### Using Docker Compose (Recommended)

The project includes a `docker-compose.yml` that sets up both the application and a PostgreSQL database.

```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (⚠️ deletes database data)
docker-compose down -v
```

The application will be available at `http://localhost:8000` with PostgreSQL running on port `5432`.

### Using Docker Only

```bash
# Build the image
docker build -t fastapi-base .

# Run the container
docker run -d -p 8000:8000 \
  -e DATABASE_URL="sqlite:///./app.db" \
  -e SECRET_KEY="your-secret-key" \
  fastapi-base
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///./app.db` | Yes |
| `SECRET_KEY` | JWT signing secret key | - | Yes |
| `ALGORITHM` | JWT algorithm | `HS256` | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `30` | No |
| `BCRYPT_ROUNDS` | Bcrypt hashing rounds for passwords | `10` | No |
| `CHATBOT_QUERY_LIMIT` | Max chatbot queries per user | `5` | No |
| `CHATBOT_QUERY_WINDOW_HOURS` | Rate limit window in hours | `24` | No |
| `OPENAI_API_KEY` | OpenAI API key for LangGraph agent | - | Yes (for chatbot) |
| `LANGSMITH_TRACING` | Enable LangSmith tracing | `false` | No |
| `LANGSMITH_API_KEY` | LangSmith API key for monitoring | - | No |

**Generate a secure SECRET_KEY:**
```bash
openssl rand -hex 32
# or using Python:
python -c "import secrets; print(secrets.token_hex(32))"
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- LangSmith: https://smith.langchain.com/

## Troubleshooting

### "Module not found" errors
Make sure you're in the virtual environment and have installed all dependencies:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt
```

Or simply run:
```bash
uv sync
```

### Database connection errors
- Check that `DATABASE_URL` is correctly set in `.env`
- For SQLite, ensure the directory is writable
- For PostgreSQL/MySQL, verify the server is running and credentials are correct

### "Could not validate credentials" errors
- Ensure you're sending the token in the `Authorization: Bearer <token>` header
- Check that the token hasn't expired (default: 30 minutes)
- Verify `SECRET_KEY` in `.env` matches the one used to generate the token

### Alembic migration issues
```bash
# Reset migrations (⚠️ development only)
rm -rf alembic/versions/*.py
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

### LangGraph agent errors

**"OpenAI API key not found"**
- Ensure `OPENAI_API_KEY` is set in your `.env` file
- Verify the key is valid and has credits available

**"Checkpointer not initialized"**
- Make sure the PostgreSQL database is running
- Check the `DB_URI` in `src/db/checkpoint.py` is correct
- Verify the database is accessible

**"langgraph dev" command not found**
- Install LangGraph CLI: `uv pip install langgraph-cli`
- Ensure you're in the virtual environment

**Agent not responding or timing out**
- Check your OpenAI API key has sufficient credits
- Verify internet connection for API calls
- Check LangSmith dashboard for error traces (if enabled)

### Windows-specific errors

**"Psycopg cannot use the 'ProactorEventLoop' to run in async mode"**

This error occurs on Windows when using uvicorn directly without the correct event loop configuration.

**Solution 1 (Recommended):**
```bash
python run.py
```

**Solution 2:**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --loop asyncio
```

**Why this happens:**
- Windows uses `ProactorEventLoop` by default (Python 3.8+)
- The async PostgreSQL driver (psycopg) requires `SelectorEventLoop`
- The `run.py` script automatically configures the correct event loop
- Linux/macOS don't have this issue as they use `SelectorEventLoop` by default

**Note:** This only affects local development on Windows. Railway and Docker deployments use Linux containers and work without any special configuration.

## Project Status

This is a **production-ready template** that includes:
- ✅ JWT authentication with secure password hashing (bcrypt)
- ✅ LangGraph AI agents with state persistence
- ✅ Streaming and non-streaming chatbot endpoints
- ✅ Per-user rate limiting for chatbot endpoints (5 queries/24 hours)
- ✅ Usage tracking and statistics
- ✅ PostgreSQL checkpointing for conversation history
- ✅ LangSmith integration for tracing and monitoring
- ✅ Modular architecture following best practices
- ✅ Complete test suite with 85%+ coverage
- ✅ Database migrations with Alembic
- ✅ Docker support for easy deployment
- ✅ Comprehensive API documentation
- ✅ CORS configuration
- ✅ Input validation with Pydantic
- ✅ Role-based access control (staff, superuser)
- ✅ Configurable rate limiting via environment variables

## Contributing

This is a template project. Feel free to:
- Fork and customize for your needs
- Report issues or suggest improvements
- Use as a starting point for your projects

## License

This is a template project - use it as you wish for your own projects.
