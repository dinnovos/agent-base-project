from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.routers import auth, users, profiles, chatbot
from src.db.database import engine
from src.models.base import Base
from src.models import user, profile  # Import models to ensure they're registered
from src.core.logging import setup_logging
from src.db.checkpoint import lifespan

setup_logging()
# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="{{cookiecutter.project_name}}",
    description="{{cookiecutter.description}}",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure rate limiter
app.state.limiter = chatbot.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(chatbot.router)

@app.get("/", tags=["Root"])
def root():
    """Root endpoint - health check."""
    return {
        "message": "{{cookiecutter.project_name}}",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
