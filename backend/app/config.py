from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Agente Monitoramento Carteirinhas"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/carteirinhas_db"
    CORS_ORIGINS: str = "http://localhost:3000,https://*.vercel.app"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
