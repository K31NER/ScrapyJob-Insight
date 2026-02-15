from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY_GROQ: str
    DATA_LAKE_DB_URI: str
    
    class Config:
        env_file = ".env"

settings = Settings()