"""
Сервис для аутентификации
РАЗРАБОТЧИК: BAGA
"""
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from src.models.user import User
from src.utils.security import hash_password, verify_password
from src.utils.validators import validate_password_strength, validate_age


class AuthService:
    """Сервис для работы с аутентификацией"""
    
    @staticmethod
    def create_user(
        db: Session,
        email: str,
        password: str,
        name: str,
        birth_date: date
    ) -> tuple[Optional[User], Optional[str]]:
        """
        Создает нового пользователя
        
        TODO (BAGA):
        1. Проверить, что email не занят
        2. Валидировать пароль
        3. Проверить возраст (18+)
        4. Создать пользователя с хешированным паролем
        5. Вернуть (User, None) или (None, error_message)
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def verify_user(db: Session, email: str) -> Optional[User]:
        """
        Подтверждает email пользователя
        
        TODO (BAGA):
        1. Найти пользователя по email
        2. Установить is_verified=True
        3. Сохранить изменения
        4. Вернуть пользователя
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ) -> tuple[Optional[User], Optional[str]]:
        """
        Аутентифицирует пользователя
        
        TODO (BAGA):
        1. Найти пользователя по email
        2. Проверить пароль
        3. Проверить is_verified
        4. Вернуть (User, None) или (None, error_message)
        """
        # TODO: Implement
        pass


