"""
Схемы для аутентификации и авторизации
РАЗРАБОТЧИК: BAGA
"""
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional
from src.constants.constants import AccountType


class SignUpRequest(BaseModel):
    """Запрос на регистрацию"""
    email: EmailStr
    password: str
    name: str
    birth_date: date


class VerifyEmailRequest(BaseModel):
    """Запрос на верификацию email"""
    email: EmailStr
    otp_code: str


class SignInRequest(BaseModel):
    """Запрос на вход"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Ответ с данными пользователя"""
    id: int
    name: str
    birth_date: date
    account_type: AccountType
    
    class Config:
        from_attributes = True


class SignUpResponse(BaseModel):
    """Ответ на регистрацию"""
    message: str
    email: str


class SignInResponse(BaseModel):
    """Ответ на вход"""
    message: str
    user: UserResponse


