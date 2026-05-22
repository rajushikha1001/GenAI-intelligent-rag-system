from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    CHROMA_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()