"""
Application configuration loaded from environment variables.
"""

import os
from functools import lru_cache

import urllib.parse

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database connection variables
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: str = "5432"
    DB_NAME: str = ""
    
    # JWT settings
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    def __init__(self, **values):
        values.setdefault("_env_file", None)
        super().__init__(**values)

    @property
    def DATABASE_URL(self) -> str:
        # URL-encode password to handle special characters
        encoded_password = urllib.parse.quote(self.DB_PASSWORD, safe="")
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{encoded_password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings(_env_file=".env")
