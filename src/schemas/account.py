"""
Схемы для банковских счетов
РАЗРАБОТЧИК: EZIRA
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BankInfo(BaseModel):
    """Информация о банке"""
    id: int
    name: str


class AccountCreateRequest(BaseModel):
    """Запрос на создание счета"""
    client_id: int


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
    account_id: str
    client_id: int
    client_name: str
    account_name: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class AccountListResponse(BaseModel):
    """Список счетов"""
    accounts: List[AccountResponse]


class ConsentRequest(BaseModel):
    """Запрос на создание consent"""
    bank_id: int
    permissions: List[str]  # ["accounts", "balances", "transactions"]
