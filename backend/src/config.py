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
        
        # Логируем SMTP настройки для отладки
        print(f"📧 SMTP Configuration:")
        print(f"   SMTP_ENABLED: {self.SMTP_ENABLED} (type: {type(self.SMTP_ENABLED)})")
        print(f"   SMTP_HOST: {self.SMTP_HOST}")
        print(f"   SMTP_PORT: {self.SMTP_PORT}")
        print(f"   SMTP_USERNAME: {self.SMTP_USERNAME[:3]}***" if self.SMTP_USERNAME else "   SMTP_USERNAME: (empty)")
        print(f"   SMTP_FROM_EMAIL: {self.SMTP_FROM_EMAIL}")
        
        # Явно преобразуем SMTP_ENABLED из строки в булево значение, если нужно
        env_smtp_enabled = os.getenv("SMTP_ENABLED", "")
        if env_smtp_enabled:
            if isinstance(env_smtp_enabled, str):
                self.SMTP_ENABLED = env_smtp_enabled.lower() in ("true", "1", "yes", "on")
                print(f"   SMTP_ENABLED converted from string '{env_smtp_enabled}' to {self.SMTP_ENABLED}")
        
        # Проверяем, что SMTP_USERNAME тоже загружен из переменных окружения
        env_smtp_username = os.getenv("SMTP_USERNAME", "")
        if env_smtp_username:
            self.SMTP_USERNAME = env_smtp_username
            print(f"   SMTP_USERNAME loaded from environment variable")
        
        env_smtp_password = os.getenv("SMTP_PASSWORD", "")
        if env_smtp_password:
            self.SMTP_PASSWORD = env_smtp_password
            print(f"   SMTP_PASSWORD loaded from environment variable")
        
        env_smtp_host = os.getenv("SMTP_HOST", "")
        if env_smtp_host:
            self.SMTP_HOST = env_smtp_host
            print(f"   SMTP_HOST loaded from environment variable: {self.SMTP_HOST}")
        
        env_smtp_port = os.getenv("SMTP_PORT", "")
        if env_smtp_port:
            try:
                self.SMTP_PORT = int(env_smtp_port)
                print(f"   SMTP_PORT loaded from environment variable: {self.SMTP_PORT}")
            except ValueError:
                print(f"   ⚠️ Invalid SMTP_PORT: {env_smtp_port}")
        
        env_smtp_from_email = os.getenv("SMTP_FROM_EMAIL", "")
        if env_smtp_from_email:
            self.SMTP_FROM_EMAIL = env_smtp_from_email
            print(f"   SMTP_FROM_EMAIL loaded from environment variable: {self.SMTP_FROM_EMAIL}")

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
