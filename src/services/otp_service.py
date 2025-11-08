"""
Сервис для работы с OTP кодами
РАЗРАБОТЧИК: BAGA
"""
import redis
from typing import Optional

from src.config import settings


class OTPService:
    """Сервис для работы с OTP кодами"""
    
    @staticmethod
    def generate_and_save_otp(redis_client: redis.Redis, email: str) -> str:
        """
        Генерирует и сохраняет OTP код
        
        TODO (BAGA):
        1. Получить OTP код из settings (хардкод или генерация)
        2. Сохранить в Redis: otp:{email} -> код
        3. Установить TTL = OTP_EXPIRE_MINUTES * 60
        4. Вернуть код
        """
        # TODO: Implement
        otp_code = settings.OTP_CODE
        return otp_code
    
    @staticmethod
    def verify_otp(redis_client: redis.Redis, email: str, code: str) -> bool:
        """
        Проверяет OTP код
        
        TODO (BAGA):
        1. Получить сохраненный код из Redis по ключу otp:{email}
        2. Сравнить с переданным кодом
        3. Если совпадает - удалить из Redis
        4. Вернуть True/False
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def send_otp_email(email: str, code: str) -> bool:
        """
        Отправляет OTP код на email (опционально)
        
        TODO (BAGA - опционально):
        1. Настроить SMTP или использовать сервис (SendGrid, etc)
        2. Отправить email с кодом
        3. Вернуть True если успешно
        """
        # TODO: Implement (optional)
        pass


