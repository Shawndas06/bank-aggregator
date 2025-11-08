"""
Функции для работы с безопасностью (хеширование паролей и т.д.)
"""
from passlib.context import CryptContext

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хеширует пароль.
    
    Args:
        password: Пароль в открытом виде
    
    Returns:
        str: Хешированный пароль
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля хешу.
    
    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хешированный пароль
    
    Returns:
        bool: True если пароль совпадает
    """
    return pwd_context.verify(plain_password, hashed_password)


