"""
Сервис для работы с сессиями
"""
import secrets
import logging
from typing import Optional
import redis

from src.config import settings

logger = logging.getLogger(__name__)


class SessionService:
    """Сервис для работы с сессиями в Redis"""
    
    @staticmethod
    def create_session(redis_client: redis.Redis, user_id: int) -> str:
        """
        Создаёт новую сессию для пользователя
        
        Returns:
            session_id для установки в cookie
        """
        session_id = secrets.token_urlsafe(32)
        session_key = f"session:{session_id}"
        
        # Сохраняем в Redis с TTL
        ttl = settings.SESSION_EXPIRE_HOURS * 3600
        redis_client.setex(session_key, ttl, str(user_id))
        
        logger.info(f"Создана сессия для пользователя {user_id}")
        return session_id
    
    @staticmethod
    def get_user_id(redis_client: redis.Redis, session_id: str) -> Optional[int]:
        """
        Получает user_id по session_id
        
        Returns:
            user_id или None если сессия не найдена/истекла
        """
        session_key = f"session:{session_id}"
        user_id_str = redis_client.get(session_key)
        
        if user_id_str:
            return int(user_id_str)
        return None
    
    @staticmethod
    def delete_session(redis_client: redis.Redis, session_id: str) -> bool:
        """
        Удаляет сессию
        
        Returns:
            True если успешно удалено
        """
        session_key = f"session:{session_id}"
        result = redis_client.delete(session_key)
        
        if result:
            logger.info(f"Сессия удалена: {session_id[:10]}...")
        return result > 0
