from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tersu Todo"
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    PROJECT_DESCRIPTION: str = "A simple todo with fastapi"
    PROJECT_VERSION: str = "v1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FRONTEND_ORIGIN: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
