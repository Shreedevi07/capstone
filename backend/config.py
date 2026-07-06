import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str | None = None
    github_token: str | None = None
    port: int = 8000
    host: str = "0.0.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
