"""
Схемы для аутентификации и авторизации
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date
from typing import Optional
from src.constants.constants import AccountType


class SignUpRequest(BaseModel):
    """Запрос на регистрацию"""
    model_config = ConfigDict(populate_by_name=True)
    
    email: EmailStr
    password: str
    name: str
    birth_date: date = Field(..., alias='birthDate')


class VerifyEmailRequest(BaseModel):
    """Запрос на верификацию email"""
    model_config = ConfigDict(populate_by_name=True)
    
    email: EmailStr
    code: str = Field(..., alias='otpCode')


class SignInRequest(BaseModel):
    """Запрос на вход"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Ответ с данными пользователя"""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    id: int
    name: str
    birth_date: date = Field(..., serialization_alias='birthDate')
    account_type: AccountType = Field(..., serialization_alias='accountType')


class SignUpResponse(BaseModel):
    """Ответ на регистрацию"""
    message: str
    email: str


class SignInResponse(BaseModel):
    """Ответ на вход"""
    message: str
    user: UserResponse
