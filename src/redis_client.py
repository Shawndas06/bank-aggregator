"""
Клиент для работы с Redis
"""
import redis
from typing import Optional
from src.config import settings

# Создаем клиент Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
    decode_responses=True
)


def get_redis() -> redis.Redis:
    """
    Dependency для получения клиента Redis.
    Используется в FastAPI эндпоинтах.
    """
    return redis_client


def set_with_expiry(key: str, value: str, expiry_seconds: int) -> bool:
    """
    Устанавливает значение в Redis с временем жизни.
    
    Args:
        key: Ключ
        value: Значение
        expiry_seconds: Время жизни в секундах
    
    Returns:
        bool: True если успешно
    """
    return redis_client.setex(key, expiry_seconds, value)


def get_value(key: str) -> Optional[str]:
    """
    Получает значение из Redis.
    
    Args:
        key: Ключ
    
    Returns:
        Optional[str]: Значение или None
    """
    return redis_client.get(key)


def delete_key(key: str) -> bool:
    """
    Удаляет ключ из Redis.
    
    Args:
        key: Ключ
    
    Returns:
        bool: True если ключ был удален
    """
    return redis_client.delete(key) > 0


