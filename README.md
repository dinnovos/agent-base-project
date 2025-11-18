# FastAPI Base Project

A modular FastAPI project template with JWT authentication, SQLAlchemy ORM, and Alembic migrations.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy ORM** - Powerful database ORM with support for multiple databases
- **JWT Authentication** - Secure authentication using JSON Web Tokens
- **Alembic** - Database migration management
- **Modular Architecture** - Clean separation of concerns with routers, services, and models
- **Pydantic Schemas** - Request/response validation and serialization
- **CORS Support** - Cross-Origin Resource Sharing enabled
- **Base Models** - Pre-built User and Profile models with relationships

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
│   │   └── session.py       # Database session management
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
│   │   ├── users.py         # User management routes
│   │   └── profiles.py      # Profile routes
│   └── dependencies.py      # Shared dependencies (auth, etc.)
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

Follow these steps to set up and run the project:

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv
```

### Step 2: Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
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
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Generate a secure SECRET_KEY:**
```bash
# Using openssl
openssl rand -hex 32

# Or using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

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

**Option 1: Using the run script**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
# Development mode with auto-reload
uvicorn src.main:app --reload

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **URL**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

---

## Alternative Setup Methods

### Using Docker Compose

If you prefer using Docker:

```bash
docker-compose up
```

This will start both the application and a PostgreSQL database.

### Using Makefile (Linux/Mac)

If you have `make` installed:

```bash
make install    # Install dependencies
make dev        # Run development server
```

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

## Useful Commands (Makefile)

If you have `make` installed (Linux/Mac), you can use these shortcuts:

```bash
make help        # Show all available commands
make install     # Install dependencies
make dev         # Run development server
make test        # Run tests
make clean       # Clean cache and build files
make migrate     # Create new migration (interactive)
make upgrade     # Apply migrations
make downgrade   # Rollback last migration
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///./app.db` | Yes |
| `SECRET_KEY` | JWT signing secret key | - | Yes |
| `ALGORITHM` | JWT algorithm | `HS256` | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `30` | No |

**Generate a secure SECRET_KEY:**
```bash
openssl rand -hex 32
# or using Python:
python -c "import secrets; print(secrets.token_hex(32))"
```

## Troubleshooting

### "Module not found" errors
Make sure you're in the virtual environment and have installed all dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
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

## Project Status

This is a **production-ready template** that includes:
- ✅ JWT authentication with secure password hashing
- ✅ Modular architecture following best practices
- ✅ Complete test suite with 85%+ coverage
- ✅ Database migrations with Alembic
- ✅ Docker support for easy deployment
- ✅ Comprehensive API documentation
- ✅ CORS configuration
- ✅ Input validation with Pydantic
- ✅ Role-based access control (staff, superuser)

## Contributing

This is a template project. Feel free to:
- Fork and customize for your needs
- Report issues or suggest improvements
- Use as a starting point for your projects

## License

This is a template project - use it as you wish for your own projects.
