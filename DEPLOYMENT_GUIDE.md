# Deployment Guide - Windows vs Production

## Quick Reference

| Environment | Command | Notes |
|-------------|---------|-------|
| **Windows Dev** | `python run.py` | ✅ Recommended |
| **Windows Dev** | `uvicorn src.main:app --reload --loop asyncio` | ✅ Alternative |
| **Linux/macOS Dev** | `uvicorn src.main:app --reload` | ✅ Works normally |
| **Railway** | `uvicorn src.main:app --host 0.0.0.0 --port 8000` | ✅ No special config |
| **Docker** | `uvicorn src.main:app --host 0.0.0.0 --port 8000` | ✅ No special config |
| **Windows Server** | `uvicorn src.main:app --host 0.0.0.0 --port 8000 --loop asyncio` | ⚠️ Needs --loop |

---

## Development Setup

### Windows

```bash
# 1. Install dependencies
uv sync

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Configure environment
copy .env.example .env
# Edit .env with your settings

# 4. Initialize database
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

# 5. Run the application
python run.py
```

### Linux/macOS

```bash
# 1. Install dependencies
uv sync

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Initialize database
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

# 5. Run the application
python run.py
# or
uvicorn src.main:app --reload
```

---

## Production Deployment

### Railway

**No special configuration needed!** Railway uses Linux containers.

Your `Dockerfile` is already correctly configured:

```dockerfile
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deployment steps:**

1. Push your code to GitHub
2. Connect Railway to your repository
3. Railway will automatically:
   - Build using your Dockerfile
   - Deploy to a Linux container
   - Work without any Windows-specific fixes

**Environment variables to set in Railway:**
- `DATABASE_URL` - Your PostgreSQL connection string
- `SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `OPENAI_API_KEY` - Your OpenAI API key
- `LANGSMITH_API_KEY` - (Optional) For tracing

### Docker

```bash
# Build
docker build -t agent-base-project .

# Run
docker run -d -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e SECRET_KEY="your-secret-key" \
  -e OPENAI_API_KEY="sk-..." \
  agent-base-project
```

Or using Docker Compose:

```bash
docker-compose up -d
```

### Linux/macOS Server

**Standard deployment:**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**With Gunicorn (recommended for production):**
```bash
gunicorn src.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Windows Server (if needed)

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --loop asyncio
```

---

## Why the Difference?

### The Problem

- **Windows** (Python 3.8+) uses `ProactorEventLoop` as the default async event loop
- **psycopg** (async PostgreSQL driver) requires `SelectorEventLoop` for compatibility
- **Linux/macOS** use `SelectorEventLoop` by default, so no issue

### The Solution

The project includes two fixes:

1. **`run.py`** - Sets the correct event loop before starting uvicorn:
   ```python
   if sys.platform == 'win32':
       asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
   ```

2. **`src/main.py`** - Backup fix for direct imports:
   ```python
   if sys.platform == 'win32':
       asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
   ```

### Platform Behavior

| Platform | Default Event Loop | Needs Fix? |
|----------|-------------------|------------|
| Windows | ProactorEventLoop | ✅ Yes |
| Linux | SelectorEventLoop | ❌ No |
| macOS | SelectorEventLoop | ❌ No |
| Docker (any host) | SelectorEventLoop (Linux container) | ❌ No |
| Railway | SelectorEventLoop (Linux container) | ❌ No |

---

## Troubleshooting

### Error: "Psycopg cannot use the 'ProactorEventLoop'"

**On Windows development:**
```bash
# Solution 1 (Recommended)
python run.py

# Solution 2
uvicorn src.main:app --reload --loop asyncio
```

**On Railway/Docker:**
- This error should NEVER occur
- If it does, check that you're using the Dockerfile (not running Windows directly)

### Error: "uvicorn: command not found"

Make sure virtual environment is activated:
```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### Server starts but crashes immediately

Check your `.env` file has all required variables:
- `DATABASE_URL`
- `SECRET_KEY`
- `OPENAI_API_KEY`

---

## Best Practices

### Development
- ✅ Use `python run.py` on all platforms (consistent)
- ✅ Use `--reload` for auto-reloading during development
- ✅ Use SQLite for local development (faster, simpler)

### Production
- ✅ Use PostgreSQL (required for LangGraph checkpointing)
- ✅ Use environment variables for all secrets
- ✅ Use Docker/Railway for deployment (handles platform differences)
- ✅ Use Gunicorn with uvicorn workers on Linux (better performance)
- ✅ Set proper `BCRYPT_ROUNDS` (10 for dev, 12+ for production)

### Security
- ✅ Generate a strong `SECRET_KEY`: `openssl rand -hex 32`
- ✅ Never commit `.env` file
- ✅ Use different secrets for dev/staging/production
- ✅ Rotate API keys regularly

---

## Summary

**For Development:**
- Windows → Use `python run.py`
- Linux/macOS → Use `python run.py` or `uvicorn src.main:app --reload`

**For Production:**
- Railway → No changes needed, works out of the box
- Docker → No changes needed, works out of the box
- Linux Server → Standard uvicorn or gunicorn
- Windows Server → Add `--loop asyncio` parameter

**The key takeaway:** Railway and Docker deployments are NOT affected by the Windows issue because they run Linux containers.
