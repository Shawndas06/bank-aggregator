"""
Константы приложения
"""
from enum import Enum


class AccountType(str, Enum):
    """Типы аккаунтов"""
    FREE = "free"
    PREMIUM = "premium"


class BankId(int, Enum):
    """ID банков"""
    VBANK = 1
    SBANK = 2
    ABANK = 3


class BankName(str, Enum):
    """Названия банков"""
    VBANK = "vbank"
    SBANK = "sbank"
    ABANK = "abank"


class InvitationStatus(str, Enum):
    """Статусы приглашений"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class ConsentType(str, Enum):
    """Типы согласий для банковских API"""
    ACCOUNTS = "accounts"
    BALANCES = "balances"
    TRANSACTIONS = "transactions"


# Лимиты для типов аккаунтов
ACCOUNT_LIMITS = {
    "free": {
        "maxGroups": 1,
        "maxMembers": 2
    },
    "premium": {
        "maxGroups": 5,
        "maxMembers": 20
    },
    AccountType.FREE: {
        "max_groups": 1,
        "max_members": 2
    },
    AccountType.PREMIUM: {
        "max_groups": 5,
        "max_members": 20
    }
}


# Маппинг ID банков к их названиям
BANK_ID_TO_NAME = {
    BankId.VBANK: BankName.VBANK,
    BankId.SBANK: BankName.SBANK,
    BankId.ABANK: BankName.ABANK,
}


# Маппинг названий банков к их ID
BANK_NAME_TO_ID = {
    BankName.VBANK: BankId.VBANK,
    BankName.SBANK: BankId.SBANK,
    BankName.ABANK: BankId.ABANK,
}


