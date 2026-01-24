from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Biblioteca Recursos API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-to-a-secure-random-value"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
