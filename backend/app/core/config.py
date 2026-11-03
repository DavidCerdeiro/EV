from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configuration class for the application settings. 
    """
    # API Keys
    GROQ_API_KEY: str
    
    # General configuration
    PROJECT_NAME: str = "Asistente E.V. API"
    VERSION: str = "0.1.0"
    
    # CORS configuration
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()