"""
Сервис для работы с OTP кодами
"""
import logging
import random
from sqlalchemy.orm import Session
from typing import Optional

from src.models.otp_code import OTPCode
from src.config import settings

logger = logging.getLogger(__name__)


class OTPService:
    """Сервис для работы с OTP кодами"""
    
    @staticmethod
    def generate_otp_code(db: Session, email: str) -> str:
        """
        Генерирует и сохраняет OTP код
        
        Returns:
            Код для отправки на email
        """
        # Генерируем код (используем хардкод из настроек или генерируем)
        if settings.OTP_CODE and settings.DEBUG:
            code = settings.OTP_CODE
        else:
            code = str(random.randint(100000, 999999))
        
        # Создаём OTP
        otp = OTPCode(
            email=email,
            code=code,
            expires_at=OTPCode.create_expiry_time()
        )
        
        db.add(otp)
        db.commit()
        
        logger.info(f"Создан OTP код для {email}: {code}")
        return code
    
    @staticmethod
    def verify_otp(db: Session, email: str, code: str) -> tuple[bool, Optional[str]]:
        """
        Проверяет OTP код
        
        Returns:
            (True, None) если код валиден
            (False, error_message) если код невалиден
        """
        # Находим последний неиспользованный код
        otp = (
            db.query(OTPCode)
            .filter(OTPCode.email == email, OTPCode.is_used == False)
            .order_by(OTPCode.created_at.desc())
            .first()
        )
        
        if not otp:
            return False, "OTP код не найден"
        
        # Проверяем валидность
        if not otp.is_valid(code):
            if otp.is_expired():
                return False, "OTP код истёк. Запросите новый код"
            return False, "Неверный OTP код"
        
        # Помечаем как использованный
        otp.is_used = True
        db.commit()
        
        logger.info(f"OTP код успешно проверен для {email}")
        return True, None
    
    @staticmethod
    def send_otp_email(email: str, code: str):
        """
        Отправляет OTP код на email
        
        В режиме разработки просто логируем
        """
        logger.info(f"📧 OTP код для {email}: {code}")
        logger.info(f"💡 В режиме разработки - используйте этот код для подтверждения")
        
        # TODO: Реальная отправка email (SendGrid, AWS SES и т.д.)
