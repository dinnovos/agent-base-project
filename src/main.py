from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth, users, profiles, chatbot
from src.db.database import engine
from src.models.base import Base
from src.models import user, profile  # Import models to ensure they're registered

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Base Project",
    description="A modular FastAPI project with JWT authentication and SQLAlchemy",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(chatbot.router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - health check."""
    return {
        "message": "FastAPI Base Project",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
