"""
Конфигурация банков для хакатона
"""
from typing import Dict

# URL банков из хакатона
BANK_URLS = {
    1: "https://vbank.open.bankingapi.ru",  # VBank
    2: "https://sbank.open.bankingapi.ru",  # SBank
    3: "https://abank.open.bankingapi.ru",  # ABank
}

# Названия банков
BANK_NAMES = {
    1: "vbank",
    2: "sbank",
    3: "abank"
}

# Маппинг названий к ID
BANK_NAME_TO_ID = {
    "vbank": 1,
    "sbank": 2,
    "abank": 3
}


def get_bank_url(bank_id: int) -> str:
    """Получить URL банка по ID"""
    return BANK_URLS.get(bank_id, BANK_URLS[1])


def get_bank_name(bank_id: int) -> str:
    """Получить название банка по ID"""
    return BANK_NAMES.get(bank_id, "vbank")

