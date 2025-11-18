# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **FastAPI project template** designed to be built by AI agents. The repository contains architectural specifications in `fastapi.md` that define how to construct a complete FastAPI backend with SQLAlchemy ORM and JWT authentication.

**Key Principle**: This is NOT an existing codebase to modify, but a **blueprint for generating** a new FastAPI project structure. The `fastapi.md` file is the source of truth.

## Project Architecture (from fastapi.md)

The target architecture follows a layered, modular design:

```
my_project/
├── src/
│   ├── main.py              # FastAPI entry point
│   ├── core/                # Configuration, security, constants
│   ├── db/                  # Database engine & session management
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic schemas (input/output)
│   ├── services/            # Business logic layer
│   ├── routers/             # API endpoints (grouped by domain)
│   └── dependencies.py      # Shared dependencies (auth, etc.)
├── alembic/                 # Database migrations
└── tests/                   # Unit and integration tests
```

### Core Design Patterns

**Layered Architecture**:
- **Routers** → handle HTTP requests/responses only
- **Services** → contain all business logic (no FastAPI imports)
- **Models** → SQLAlchemy ORM (all inherit from `Base`)
- **Schemas** → Pydantic models for validation

**Mandatory Base Models**:
The project MUST include these two foundational models with exact structure defined in fastapi.md:
- `User` (src/models/user.py) - authentication & user management
- `Profile` (src/models/profile.py) - user profile data with 1-to-1 relationship

### Critical Conventions (from Section 3.1)

1. **All models inherit from `Base`** declared in `src/models/base.py`
2. **Each model gets its own file** in `src/models/`
3. **Relationships must be bidirectional** when applicable
4. **No business logic in routers** - only in services
5. **Database access only via `Depends(get_db)`**
6. **JWT tokens use `sub = user.email`**
7. **Passwords must be hashed** (bcrypt via passlib)

### Pydantic Schema Standards (from Section 3.2)

Always create three schema types:
- `Create` - for input on creation
- `Update` - for partial updates
- `Read` - for output/responses

All schemas must include: `class Config: orm_mode = True`

## Dependencies

```
fastapi
uvicorn[standard]
sqlalchemy
alembic
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
pydantic
```

## Configuration

Uses Pydantic BaseSettings with `.env` file:
- `DATABASE_URL` - SQLAlchemy connection string
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration (default: 30)

## Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## API Endpoints Structure

Endpoints are organized by domain:

**`/auth`** (authentication):
- `POST /auth/token` - login, returns JWT
- `POST /auth/register` - user registration

**`/users`** (user management):
- `GET /users/me` - current user info
- `GET /users/{id}` - get user by ID
- `PATCH /users/{id}` - update user

**`/profiles`** (user profiles):
- `GET /profiles/me` - current user's profile
- `PATCH /profiles/me` - update profile

## Security Architecture

JWT implementation (core/security.py):
- `hash_password()` - bcrypt hashing
- `verify_password()` - password verification
- `create_access_token()` - JWT generation with expiration

Authentication flow:
1. User submits credentials to `/auth/token`
2. Service validates via `verify_password()`
3. JWT created with `sub = user.email`
4. Protected routes use `get_current_user` dependency

## Service Layer Design

Services must:
- Contain all business logic
- NOT import FastAPI
- Only import: models, schemas, database utilities
- Be organized by domain (auth_service.py, user_service.py, profile_service.py)

## Testing

Use pytest with TestClient (httpx):
- Test user creation
- Test login flow
- Test invalid tokens
- Test protected routes
- Test profile operations

## Working with This Repository

**If building the project from scratch**:
1. Read `fastapi.md` sections 2-7 for complete specifications
2. Create directory structure as defined in section 2
3. Implement base models User + Profile exactly as specified in section 7
4. Follow conventions in section 3 strictly
5. Use code examples from sections 5-8 as templates

**If extending an existing implementation**:
- Verify all new models inherit from `Base`
- Keep business logic in services, not routers
- Follow the Create/Update/Read schema pattern
- Maintain bidirectional relationships in models
