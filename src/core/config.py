from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    BCRYPT_ROUNDS: int = 10

    LANGSMITH_TRACING: bool = True
    LANGSMITH_API_KEY: str = ""
    
    # Chatbot Rate Limiting (DEPRECATED - Now managed by user plans)
    # These values are kept as fallback only in case of errors
    CHATBOT_QUERY_LIMIT: int = 5  # Número máximo de consultas (fallback)
    CHATBOT_QUERY_WINDOW_HOURS: int = 24  # Ventana de tiempo en horas (fallback)

    class Config:
        env_file = ".env"


settings = Settings()
