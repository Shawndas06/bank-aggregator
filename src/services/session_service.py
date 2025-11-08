"""
Сервис для работы с сессиями
РАЗРАБОТЧИК: BAGA
"""
import secrets
import redis
from typing import Optional

from src.config import settings


class SessionService:
    """Сервис для работы с сессиями в Redis"""
    
    @staticmethod
    def create_session(redis_client: redis.Redis, user_id: int) -> str:
        """
        Создает новую сессию для пользователя
        
        TODO (BAGA):
        1. Сгенерировать уникальный session_id
        2. Сохранить в Redis: session:{session_id} -> user_id
        3. Установить TTL = SESSION_EXPIRE_HOURS
        4. Вернуть session_id
        """
        # TODO: Implement
        session_id = secrets.token_urlsafe(32)
        return session_id
    
    @staticmethod
    def get_user_id(redis_client: redis.Redis, session_id: str) -> Optional[int]:
        """
        Получает user_id по session_id
        
        TODO (BAGA):
        1. Получить user_id из Redis по ключу session:{session_id}
        2. Вернуть user_id или None
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def delete_session(redis_client: redis.Redis, session_id: str) -> bool:
        """
        Удаляет сессию
        
        TODO (BAGA):
        1. Удалить ключ session:{session_id} из Redis
        2. Вернуть True если успешно
        """
        # TODO: Implement
        pass


