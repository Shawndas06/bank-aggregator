"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Bank Aggregator API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/bank_aggregator"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "bank_aggregator"
    DATABASE_USER: str = "user"
    DATABASE_PASSWORD: str = "password"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    SESSION_EXPIRE_HOURS: int = 24
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # OTP
    OTP_CODE: str = "123456"
    OTP_EXPIRE_MINUTES: int = 10
    
    # Bank APIs
    VBANK_BASE_URL: str = "https://api.vbank.com"
    VBANK_CLIENT_ID: str = ""
    VBANK_CLIENT_SECRET: str = ""
    
    ABANK_BASE_URL: str = "https://api.abank.com"
    ABANK_CLIENT_ID: str = ""
    ABANK_CLIENT_SECRET: str = ""
    
    SBANK_BASE_URL: str = "https://api.sbank.com"
    SBANK_CLIENT_ID: str = ""
    SBANK_CLIENT_SECRET: str = ""
    
    # Cache TTL (in seconds)
    BANK_TOKEN_TTL: int = 82800  # 23 hours
    CONSENT_REQUEST_TTL: int = 14400  # 4 hours
    BANK_DATA_CACHE_TTL: int = 14400  # 4 hours
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


