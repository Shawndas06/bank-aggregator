"""
Главный файл приложения Bank Aggregator
Монолитная архитектура на FastAPI

РАЗРАБОТЧИКИ:
- BAGA: Модуль аутентификации и приглашений
- EZIRA: Модуль счетов, банковской интеграции и групп
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.config import settings
from src.database import create_tables
from src.redis_client import redis_client

# Импорт роутеров
from src.routers import auth, accounts, groups


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events для приложения
    """
    # Startup
    print("🚀 Starting Bank Aggregator API...")
    print(f"📊 Database: {settings.DATABASE_HOST}:{settings.DATABASE_PORT}")
    print(f"💾 Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    
    # Создаем таблицы (если нужно)
    create_tables()
    
    # Проверяем подключение к Redis
    try:
        redis_client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
    
    print("✨ Application started successfully!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Bank Aggregator API...")


# Создаем FastAPI приложение
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API для агрегации банковских счетов",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Глобальный обработчик исключений
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Глобальный обработчик ошибок для стандартизированного формата ответов
    """
    if settings.DEBUG:
        print(f"❌ Error: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "message": "Что-то пошло не так" if not settings.DEBUG else str(exc)
            }
        }
    )


# Подключение роутеров
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(groups.router)


# Health check эндпоинт
@app.get("/", tags=["Health"])
async def health_check():
    """
    Проверка работоспособности API
    """
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION
        }
    }


@app.get("/health", tags=["Health"])
async def health():
    """
    Детальная проверка здоровья сервисов
    """
    # Проверка Redis
    redis_status = "healthy"
    try:
        redis_client.ping()
    except:
        redis_status = "unhealthy"
    
    return {
        "success": True,
        "data": {
            "api": "healthy",
            "redis": redis_status,
            "version": settings.APP_VERSION
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )


