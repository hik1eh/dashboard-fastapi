from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    app_name : str = "Planner API"
    database_url : str = "postgresql+asyncpg://moonflow:moonflow@db:5432/moonflow"
    environment : str = "development"
    frontend_origin : str = "http://localhost:5173"
    jwt_secret : str = "local-development-only-change-before-deploy"
    jwt_algorithm : str = "HS256"
    access_token_expire_minutes : int = 1440

    @property
    def frontend_origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_origin.split(",") if origin.strip()]
    
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
