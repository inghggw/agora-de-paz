from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Ágora de Paz"
    api_v1_prefix: str = "/api/v1"

    # "memory" permite correr y probar la API sin infraestructura externa
    # (ver backend/README.md). docker-compose.yml usa "postgres".
    repository_backend: Literal["memory", "postgres"] = "memory"

    database_url: str = "postgresql+psycopg://agora:agora@localhost:5432/agora_de_paz"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
