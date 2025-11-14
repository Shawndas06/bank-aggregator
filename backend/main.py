import sys
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

try:
    from src.config import settings
    from src.database import create_tables
    from src.redis_client import redis_client
    from src.routers import auth, accounts, groups, analytics, loyalty_cards, payments, premium, savings, family_budget, verification
except Exception as e:
    print(f"❌ Error importing modules: {e}")
    print(traceback.format_exc())
    sys.exit(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Bank Aggregator API...")
    # Логируем DATABASE_URL без пароля для безопасности
    db_url_safe = settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else "not configured"
    print(f"📊 Database: {db_url_safe}")
    print(f"💾 Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    
    # Проверяем, что DATABASE_URL установлен
    if not settings.DATABASE_URL or settings.DATABASE_URL == "":
        print("❌ WARNING: DATABASE_URL is not set! Please configure it in environment variables.")

    # Database connection
    try:
        create_tables()
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        print("⚠️ Continuing without database (tables will be created on first connection)")

    # Redis connection
    try:
        redis_client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"⚠️ Redis connection failed: {e} (continuing without Redis)")

    print("✨ Application started successfully!")

    yield

    print("👋 Shutting down Bank Aggregator API...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API для агрегации банковских счетов",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
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

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(groups.router)
app.include_router(analytics.router)
app.include_router(loyalty_cards.router)
app.include_router(payments.router)
app.include_router(premium.router)
app.include_router(savings.router)
app.include_router(family_budget.router)
app.include_router(verification.router)

@app.get("/", tags=["Health"])
async def health_check():
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
    """Health check с проверкой зависимостей"""
    redis_status = "unhealthy"
    db_status = "unknown"
    
    try:
        redis_client.ping()
        redis_status = "healthy"
    except Exception as e:
        print(f"⚠️ Redis health check failed: {e}")
    
    try:
        from src.database import engine
        with engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        print(f"⚠️ Database health check failed: {e}")
        db_status = "unhealthy"

    return {
        "success": True,
        "data": {
            "api": "healthy",
            "database": db_status,
            "redis": redis_status,
            "version": settings.APP_VERSION
        }
    }

@app.get("/api/health", tags=["Health"])
async def api_health():
    """Health check через /api/ для Nginx"""
    return await health()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
