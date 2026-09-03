from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    app_name : str = "MoonDashboard API"
    database_url : str = "postgresql+asyncpg://moonflow:moonflow@db:5432/moonflow"
    environment : str = "development"
    frontend_origin : str = "http://localhost:5173"
    
    
@lru_cache
def get_settings() -> Settings:
    return Settings

settings = get_settings