"""
Сервис для аутентификации
"""
import logging
from sqlalchemy.orm import Session
from typing import Optional, Tuple
from datetime import date

from src.models.user import User
from src.utils.security import hash_password, verify_password
from src.utils.validators import validate_password_strength, validate_age

logger = logging.getLogger(__name__)


class AuthService:
    """Сервис для работы с аутентификацией"""
    
    @staticmethod
    def create_user(
        db: Session,
        email: str,
        password: str,
        name: str,
        birth_date: date
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        Создаёт нового пользователя
        
        Returns:
            (User, None) если успешно
            (None, error_message) если ошибка
        """
        # Проверяем что email не занят
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return None, "Пользователь с таким email уже существует"
        
        # Валидируем пароль
        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            return None, error_msg
        
        # Проверяем возраст
        if not validate_age(birth_date):
            return None, "Вам должно быть минимум 18 лет"
        
        # Хешируем пароль
        hashed = hash_password(password)
        
        # Создаём пользователя
        new_user = User(
            email=email,
            password_hash=hashed,
            name=name,
            birth_date=birth_date,
            is_verified=False  # Требуется подтверждение email
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"Создан новый пользователь: {email}")
        return new_user, None
    
    @staticmethod
    def verify_user(db: Session, email: str) -> Optional[User]:
        """Подтверждает email пользователя"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        
        user.is_verified = True
        db.commit()
        db.refresh(user)
        
        logger.info(f"Email подтверждён для пользователя: {email}")
        return user
    
    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        Аутентифицирует пользователя
        
        Returns:
            (User, None) если успешно
            (None, error_message) если ошибка
        """
        # Ищем пользователя
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None, "Неверный email или пароль"
        
        # Проверяем пароль
        if not verify_password(password, user.password_hash):
            return None, "Неверный email или пароль"
        
        # Проверяем что email подтверждён
        if not user.is_verified:
            return None, "Аккаунт не подтвержден. Пожалуйста, подтвердите email."
        
        logger.info(f"Пользователь авторизован: {email}")
        return user, None
