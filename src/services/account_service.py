"""
Сервис для работы с банковскими счетами
РАЗРАБОТЧИК: EZIRA
"""
from sqlalchemy.orm import Session
import redis
from typing import List, Optional, Dict, Any

from src.models.account import BankAccount
from src.models.user import User


class AccountService:
    """Сервис для работы с банковскими счетами"""
    
    @staticmethod
    def get_user_accounts(
        db: Session,
        user_id: int,
        bank_id: Optional[int] = None
    ) -> List[BankAccount]:
        """
        Получает список счетов пользователя
        
        TODO (EZIRA):
        1. Запросить счета пользователя из БД
        2. Если bank_id указан - отфильтровать
        3. Вернуть список счетов
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def create_account(
        db: Session,
        user_id: int,
        bank_id: int,
        account_id: str,
        account_name: Optional[str] = None,
        consent_id: Optional[str] = None
    ) -> BankAccount:
        """
        Создает новый счет
        
        TODO (EZIRA):
        1. Создать запись BankAccount
        2. Сохранить в БД
        3. Вернуть созданный счет
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def attach_account(
        db: Session,
        account_id: int,
        user_id: int
    ) -> tuple[bool, Optional[str]]:
        """
        Привязывает счет к пользователю
        
        TODO (EZIRA):
        1. Найти счет по ID
        2. Проверить, что счет не привязан к другому пользователю
        3. Привязать к пользователю
        4. Вернуть (True, None) или (False, error_message)
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def get_account_data_cached(
        redis_client: redis.Redis,
        cache_key: str,
        fetch_func,
        ttl: int = 14400
    ) -> Any:
        """
        Получает данные с кешированием
        
        TODO (EZIRA):
        1. Проверить наличие данных в Redis по cache_key
        2. Если есть - вернуть из кеша
        3. Если нет - вызвать fetch_func(), сохранить в кеш с TTL
        4. Вернуть данные
        """
        # TODO: Implement
        pass
