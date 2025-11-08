"""
Модель банковского счета
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base


class BankAccount(Base):
    """Модель банковского счета"""
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # ID банка (1=VBank, 2=SBank, 3=ABank)
    bank_id = Column(Integer, nullable=False, index=True)
    
    # ID счета в банке
    account_id = Column(String(255), nullable=False)
    
    # Название счета (если есть)
    account_name = Column(String(255), nullable=True)
    
    # Consent ID для доступа к данным
    consent_id = Column(String(255), nullable=True)
    
    # Флаг активности
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bank_accounts")
    
    def __repr__(self):
        return f"<BankAccount(id={self.id}, user_id={self.user_id}, bank_id={self.bank_id})>"


