"""
Клиент для работы с банковскими API
РАЗРАБОТЧИК: EZIRA
"""
import httpx
import redis
from typing import Dict, Any, Optional, List

from src.config import settings
from src.constants.constants import BankId, BankName


class BankClient:
    """Клиент для взаимодействия с банковскими API"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
    
    def _get_bank_config(self, bank_id: int) -> Dict[str, str]:
        """
        Получает конфигурацию банка
        
        TODO (EZIRA):
        1. По bank_id определить BASE_URL, CLIENT_ID, CLIENT_SECRET
        2. Вернуть словарь с конфигурацией
        """
        # TODO: Implement
        configs = {
            BankId.VBANK: {
                "base_url": settings.VBANK_BASE_URL,
                "client_id": settings.VBANK_CLIENT_ID,
                "client_secret": settings.VBANK_CLIENT_SECRET
            },
            BankId.SBANK: {
                "base_url": settings.SBANK_BASE_URL,
                "client_id": settings.SBANK_CLIENT_ID,
                "client_secret": settings.SBANK_CLIENT_SECRET
            },
            BankId.ABANK: {
                "base_url": settings.ABANK_BASE_URL,
                "client_id": settings.ABANK_CLIENT_ID,
                "client_secret": settings.ABANK_CLIENT_SECRET
            }
        }
        return configs.get(bank_id, {})
    
    async def get_bank_token(self, user_id: int, bank_id: int) -> Optional[str]:
        """
        Получает токен банка (или создает новый)
        
        TODO (EZIRA):
        1. Проверить наличие токена в Redis: bank_token:{user_id}:{bank_id}
        2. Если есть - вернуть
        3. Если нет - запросить новый токен через /auth/bank-token
        4. Сохранить в Redis с TTL = BANK_TOKEN_TTL (23 часа)
        5. Вернуть токен
        """
        # TODO: Implement
        pass
    
    async def create_consent(
        self,
        user_id: int,
        bank_id: int,
        permissions: List[str]
    ) -> Optional[str]:
        """
        Создает consent для доступа к данным
        
        TODO (EZIRA):
        1. Получить токен банка
        2. Запросить создание consent через /account-consents/requests
        3. Сохранить consent_id в Redis с TTL = CONSENT_REQUEST_TTL (4 часа)
        4. Вернуть consent_id
        """
        # TODO: Implement
        pass
    
    async def get_accounts(
        self,
        user_id: int,
        bank_id: int
    ) -> List[Dict[str, Any]]:
        """
        Получает список счетов из банка
        
        TODO (EZIRA):
        1. Получить токен банка
        2. Запросить /api/accounts
        3. Вернуть список счетов
        """
        # TODO: Implement
        pass
    
    async def get_account_details(
        self,
        user_id: int,
        bank_id: int,
        account_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Получает детальную информацию о счете
        
        TODO (EZIRA):
        1. Получить токен банка
        2. Запросить /api/accounts/{account_id}
        3. Вернуть данные счета
        """
        # TODO: Implement
        pass
    
    async def get_account_balance(
        self,
        user_id: int,
        bank_id: int,
        account_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Получает баланс счета
        
        TODO (EZIRA):
        1. Получить токен банка
        2. Запросить /api/accounts/{account_id}/balances
        3. Вернуть баланс
        """
        # TODO: Implement
        pass
    
    async def get_account_transactions(
        self,
        user_id: int,
        bank_id: int,
        account_id: str
    ) -> List[Dict[str, Any]]:
        """
        Получает транзакции счета
        
        TODO (EZIRA):
        1. Получить токен банка
        2. Запросить /api/accounts/{account_id}/transactions
        3. Вернуть список транзакций
        """
        # TODO: Implement
        pass


