from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from src.config import settings

# Проверяем наличие DATABASE_URL
if not settings.DATABASE_URL or settings.DATABASE_URL == "":
    raise ValueError(
        "DATABASE_URL is not configured! "
        "Please set DATABASE_URL environment variable. "
        "Example: postgresql://user:password@host:5432/dbname"
    )

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
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
        
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
    except OperationalError as e:
        print(f"⚠️ Database connection error: {e}")
        print("⚠️ Tables will be created on first database connection")
        # Не падаем, таблицы создадутся при первом подключении
    except Exception as e:
        print(f"⚠️ Database error: {e}")
        print("⚠️ Tables will be created on first database connection")
        # Не падаем, продолжаем работу
