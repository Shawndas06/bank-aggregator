from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Bank Aggregator API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = ""  # Должен быть установлен через переменные окружения
    DATABASE_HOST: str = "postgres"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "bank_aggregator"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"
    
    def __init__(self, **kwargs):
        import os
        super().__init__(**kwargs)
        # Проверяем, установлена ли переменная окружения DATABASE_URL
        env_db_url = os.getenv("DATABASE_URL", "")
        if env_db_url:
            self.DATABASE_URL = env_db_url
            print(f"✅ DATABASE_URL loaded from environment variable")
        # Если DATABASE_URL не установлен и мы не в Docker Compose (где postgres доступен), НЕ строим из компонентов
        elif not self.DATABASE_URL or self.DATABASE_URL == "":
            # Только для локальной разработки с Docker Compose строим из компонентов
            # В продакшене (Render.com) это не должно работать
            print(f"⚠️ WARNING: DATABASE_URL not set in environment variables!")
            print(f"⚠️ Current DATABASE_URL: {self.DATABASE_URL}")
            print(f"⚠️ Environment DATABASE_URL: {env_db_url}")
            # НЕ строим автоматически, пусть будет пустым

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    SESSION_EXPIRE_HOURS: int = 24

    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:5174"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    OTP_CODE: str = "123456"
    OTP_EXPIRE_MINUTES: int = 10
    
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@bankapp.com"
    SMTP_FROM_NAME: str = "Bank Aggregator"
    SMTP_ENABLED: bool = False

    TEAM_CLIENT_ID: str = "team222"
    TEAM_CLIENT_SECRET: str = "Wl1F0L2aVHOPE20rM0DFeqvP9Qr2pgQT"

    VBANK_BASE_URL: str = "https://vbank.open.bankingapi.ru"
    ABANK_BASE_URL: str = "https://abank.open.bankingapi.ru"
    SBANK_BASE_URL: str = "https://sbank.open.bankingapi.ru"

    BANK_TOKEN_TTL: int = 82800
    CONSENT_REQUEST_TTL: int = 14400
    BANK_DATA_CACHE_TTL: int = 14400

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
