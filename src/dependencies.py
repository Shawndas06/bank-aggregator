"""
Общие зависимости для FastAPI эндпоинтов
"""
from fastapi import Cookie, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.redis_client import get_redis
from src.models.user import User
import redis


async def get_current_user(
    session_id: Optional[str] = Cookie(None, alias="session-id"),
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis)
) -> User:
    """
    Получает текущего пользователя из сессии.
    
    Args:
        session_id: ID сессии из cookie
        db: Сессия базы данных
        redis_client: Клиент Redis
    
    Returns:
        User: Объект пользователя
    
    Raises:
        HTTPException: Если пользователь не авторизован
    """
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Получаем user_id из Redis
    user_id = redis_client.get(f"session:{session_id}")
    if not user_id:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    # Получаем пользователя из БД
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


async def get_current_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Получает текущего верифицированного пользователя.
    
    Args:
        current_user: Текущий пользователь
    
    Returns:
        User: Объект пользователя
    
    Raises:
        HTTPException: Если пользователь не верифицирован
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified. Please verify your email first."
        )
    
    return current_user


