from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configuration class for the application settings. 
    """
    # API Keys
    GROQ_API_KEY: str
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # OAuth Credentials
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    # GitHub Token
    GITHUB_TOKEN: str
    
    # CORS & URLs configuration
    FRONTEND_URL: str
    BACKEND_BASE_URL: str

    # General configuration
    PROJECT_NAME: str = "Asistente E.V. API"
    VERSION: str = "0.1.0"
    
    

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Propiedades dinámicas basadas en el entorno
    @property
    def SPOTIFY_REDIRECT_URI(self) -> str:
        return f"{self.BACKEND_BASE_URL}/auth/spotify/callback"

    @property
    def GOOGLE_REDIRECT_URI(self) -> str:
        return f"{self.BACKEND_BASE_URL}/auth/google/callback"

settings = Settings()