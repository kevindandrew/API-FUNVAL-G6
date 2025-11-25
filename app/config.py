from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str
    
    # Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    # Configuración App
    APP_NAME: str = "FunVal G6 E-Commerce API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
