"""
Модель OTP кодов для подтверждения email
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from src.database import Base


class OTPCode(Base):
    """Модель OTP кода для верификации email"""
    __tablename__ = "otp_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, nullable=False)
    code = Column(String(6), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def is_expired(self) -> bool:
        """Проверка истёк ли код"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self, code: str) -> bool:
        """Проверка валидности кода"""
        return (
            self.code == code and
            not self.is_used and
            not self.is_expired()
        )
    
    @staticmethod
    def create_expiry_time() -> datetime:
        """Создаёт время истечения (10 минут от текущего момента)"""
        return datetime.utcnow() + timedelta(minutes=10)
    
    def __repr__(self):
        return f"<OTPCode(email={self.email}, expired={self.is_expired()})>"

