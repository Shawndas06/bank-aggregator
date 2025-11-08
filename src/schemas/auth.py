from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date
from typing import Optional
from src.constants.constants import AccountType

class SignUpRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    password: str
    name: str
    birth_date: date = Field(..., alias='birthDate')

class VerifyEmailRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    code: str = Field(..., alias='otpCode')

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    name: str
    birth_date: date = Field(..., serialization_alias='birthDate')
    account_type: AccountType = Field(..., serialization_alias='accountType')

class SignUpResponse(BaseModel):
    message: str
    email: str

class SignInResponse(BaseModel):
    message: str
    user: UserResponse
