import logging
import random
from sqlalchemy.orm import Session
from typing import Optional

from src.models.otp_code import OTPCode
from src.config import settings

logger = logging.getLogger(__name__)

class OTPService:

    @staticmethod
    def generate_otp_code(db: Session, email: str) -> str:
        if settings.OTP_CODE and settings.DEBUG:
            code = settings.OTP_CODE
        else:
            code = str(random.randint(100000, 999999))

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
        otp = (
            db.query(OTPCode)
            .filter(OTPCode.email == email, OTPCode.is_used == False)
            .order_by(OTPCode.created_at.desc())
            .first()
        )

        if not otp:
            return False, "OTP код не найден"

        if not otp.is_valid(code):
            if otp.is_expired():
                return False, "OTP код истёк. Запросите новый код"
            return False, "Неверный OTP код"

        otp.is_used = True
        db.commit()

        logger.info(f"OTP код успешно проверен для {email}")
        return True, None

    @staticmethod
    def send_otp_email(email: str, code: str):
        logger.info(f"📧 OTP код для {email}: {code}")
        logger.info(f"💡 В режиме разработки - используйте этот код для подтверждения")
