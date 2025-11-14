from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os

from src.config import settings

# Проверяем наличие DATABASE_URL
env_db_url = os.getenv("DATABASE_URL", "")
print(f"🔍 DEBUG: Environment DATABASE_URL exists: {bool(env_db_url)}")
print(f"🔍 DEBUG: Settings DATABASE_URL: {settings.DATABASE_URL[:50] + '...' if len(settings.DATABASE_URL) > 50 else settings.DATABASE_URL}")

if not settings.DATABASE_URL or settings.DATABASE_URL == "":
    error_msg = (
        "❌ ERROR: DATABASE_URL is not configured!\n"
        "   Please set DATABASE_URL environment variable on Render.com\n"
        "   Go to: Render.com → Your Service → Environment → Add DATABASE_URL\n"
        "   Example: postgresql://user:password@host:5432/dbname\n"
        "   Or get it from: PostgreSQL Service → Internal Database URL"
    )
    print(error_msg)
    # Не создаем engine, если DATABASE_URL не установлен
    engine = None
    SessionLocal = None
    Base = declarative_base()
    
    def get_db():
        raise RuntimeError("DATABASE_URL is not configured! Please set it in environment variables.")
    
    def create_tables():
        print("⚠️ Skipping table creation - DATABASE_URL not configured")
else:
    # DATABASE_URL установлен, создаем engine нормально
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        connect_args={
            "connect_timeout": 10,
            "options": "-c statement_timeout=5000"
        }
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables():
        try:
            # Проверяем подключение
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables created/verified")
        except OperationalError as e:
            print(f"⚠️ Database connection error: {e}")
            print("⚠️ Tables will be created on first database connection")
        except Exception as e:
            print(f"⚠️ Database error: {e}")
            print("⚠️ Tables will be created on first database connection")
