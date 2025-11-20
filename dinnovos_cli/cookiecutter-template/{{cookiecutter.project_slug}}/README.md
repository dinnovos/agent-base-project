# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Quick Start

### Prerequisites
- Python {{cookiecutter.python_version}}
- PostgreSQL (or SQLite for development)

### Installation

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
python run.py
```

The API will be available at `http://localhost:{{cookiecutter.port}}`

## Project Structure

```
{{cookiecutter.project_slug}}/
├── src/                    # Main application code
│   ├── core/              # Configuration and utilities
│   ├── db/                # Database configuration
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API endpoints
│   └── services/          # Business logic
├── agents/                # LangGraph agents
│   └── basic/            # Basic agent implementation
├── tests/                 # Test suite
├── alembic/              # Database migrations
└── run.py                # Development server entry point
```

## Author

{{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

## License

MIT
