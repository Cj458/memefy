import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # App
    SERVICE_NAME: str = os.environ.get('SERVICE_NAME')

    # Database
    DB_USER: str = os.environ.get('DB__DB_USER')
    DB_PASS: str = os.environ.get('DB__DB_PASS')
    DB_NAME: str = os.environ.get('DB__DB_NAME')
    DB_HOST: str = os.environ.get('DB__DB_HOST')
    DB_PORT: str = os.environ.get('DB__DB_PORT')

    # Database URL
    DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    HOST_IP: str = os.environ.get('HOST_IP')


def get_settings() -> Settings:
    return Settings()