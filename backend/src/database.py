from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from src.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args={
        "connect_timeout": 5,
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
            conn.execute("SELECT 1")
        
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
    except OperationalError as e:
        print(f"⚠️ Database connection error: {e}")
        # Не падаем, таблицы создадутся при первом подключении
        raise
    except Exception as e:
        print(f"⚠️ Database error: {e}")
        # Не падаем, продолжаем работу
        raise
