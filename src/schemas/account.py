"""
Схемы для банковских счетов
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class BankInfo(BaseModel):
    """Информация о банке"""
    id: int
    name: str


class AccountCreateRequest(BaseModel):
    """Запрос на создание счета"""
    model_config = ConfigDict(populate_by_name=True)
    
    client_id: int = Field(..., alias='clientId')


class AccountAttachRequest(BaseModel):
    """Запрос на привязку счета"""
    id: int


class BalanceResponse(BaseModel):
    """Баланс счета"""
    amount: float
    currency: str


class TransactionResponse(BaseModel):
    """Транзакция"""
    id: str
    amount: float
    currency: str
    description: str
    date: datetime
    type: str  # debit/credit


class AccountResponse(BaseModel):
    """Информация о счете"""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    account_id: str = Field(..., serialization_alias='accountId')
    client_id: int = Field(..., serialization_alias='clientId')
    client_name: str = Field(..., serialization_alias='clientName')
    account_name: Optional[str] = Field(None, serialization_alias='accountName')
    is_active: bool = Field(..., serialization_alias='isActive')


class AccountListResponse(BaseModel):
    """Список счетов"""
    accounts: List[AccountResponse]


class ConsentRequest(BaseModel):
    """Запрос на создание consent"""
    model_config = ConfigDict(populate_by_name=True)
    
    bank_id: int = Field(..., alias='bankId')
    permissions: List[str]
