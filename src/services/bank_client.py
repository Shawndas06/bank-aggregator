"""
Клиент для работы с банковскими API (Real Hackathon API)
"""
import logging
import httpx
from typing import Dict, Any, Optional, List
import redis
from datetime import datetime, timedelta

from src.config import settings
from src.constants.bank_config import get_bank_url, get_bank_name

logger = logging.getLogger(__name__)


class BankClient:
    """Клиент для взаимодействия с реальными банковскими API хакатона"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.timeout = httpx.Timeout(30.0, connect=10.0)
    
    def _get_bank_config(self, bank_id: int) -> Dict[str, str]:
        """Получает конфигурацию банка"""
        return {
            "base_url": get_bank_url(bank_id),
            "name": get_bank_name(bank_id),
            "client_id": settings.TEAM_CLIENT_ID,
            "client_secret": settings.TEAM_CLIENT_SECRET
        }
    
    def get_bank_token(self, user_id: int, bank_id: int) -> str:
        """
        Получает токен банка (реальный API)
        
        Endpoint: POST /auth/bank-token?client_id=team200&client_secret=xxx
        Токен живет 24 часа
        """
        token_key = f"bank_token:{user_id}:{bank_id}"
        
        # Проверяем кеш
        cached_token = self.redis_client.get(token_key)
        if cached_token:
            logger.info(f"✅ Используем кешированный токен для банка {bank_id}")
            return cached_token
        
        # Получаем новый токен от банка
        bank_config = self._get_bank_config(bank_id)
        url = f"{bank_config['base_url']}/auth/bank-token"
        
        params = {
            "client_id": bank_config["client_id"],
            "client_secret": bank_config["client_secret"]
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                token = data.get("access_token")
                
                if not token:
                    raise ValueError("Токен не получен от банка")
                
                # Сохраняем в Redis с TTL 23 часа (86400 - 1 час запас)
                self.redis_client.setex(token_key, 82800, token)
                
                logger.info(f"✅ Получен новый токен для банка {bank_id} ({bank_config['name']})")
                return token
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения токена от банка {bank_id}: {e}")
            # В режиме разработки возвращаем mock токен
            if settings.DEBUG:
                mock_token = f"mock_token_{bank_config['name']}_dev"
                logger.warning(f"⚠️  Используем mock токен для разработки")
                return mock_token
            raise
    
    def create_consent(
        self,
        user_id: int,
        bank_id: int,
        client_id: str,
        permissions: List[str]
    ) -> str:
        """
        Создаёт consent для доступа к данным клиента
        
        Endpoint: POST /account-consents/request
        Headers: X-Requesting-Bank: team200
        """
        bank_config = self._get_bank_config(bank_id)
        token = self.get_bank_token(user_id, bank_id)
        
        url = f"{bank_config['base_url']}/account-consents/request"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Requesting-Bank": bank_config["client_id"],
            "Content-Type": "application/json"
        }
        
        body = {
            "client_id": client_id,
            "permissions": permissions,
            "reason": "Агрегация счетов для Bank Aggregator",
            "requesting_bank": bank_config["client_id"],
            "requesting_bank_name": "Bank Aggregator App"
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, headers=headers, json=body)
                response.raise_for_status()
                
                data = response.json()
                consent_id = data.get("consent_id")
                consent_status = data.get("status", "unknown")
                
                if not consent_id:
                    # В SBank может быть только request_id без consent_id (pending)
                    if consent_status == "pending":
                        logger.warning(f"⚠️  Consent pending в банке {bank_id} - требуется ручное подтверждение")
                        # Используем request_id как временный consent
                        consent_id = data.get("request_id", f"pending_{bank_id}_{user_id}")
                    else:
                        raise ValueError("Consent ID не получен")
                
                # Сохраняем в Redis с TTL 4 часа
                consent_key = f"consent:{user_id}:{bank_id}"
                self.redis_client.setex(consent_key, settings.CONSENT_REQUEST_TTL, consent_id)
                
                if consent_status == "approved":
                    logger.info(f"✅ Consent {consent_id} одобрен для банка {bank_id}")
                else:
                    logger.warning(f"⚠️  Consent {consent_id} в статусе: {consent_status}")
                
                return consent_id
                
        except Exception as e:
            logger.error(f"❌ Ошибка создания consent: {e}")
            # В режиме разработки возвращаем mock consent
            if settings.DEBUG:
                mock_consent = f"consent_{bank_id}_{user_id}_dev"
                logger.warning(f"⚠️  Используем mock consent для разработки")
                return mock_consent
            raise
    
    def get_accounts(
        self,
        user_id: int,
        bank_id: int,
        client_id: str
    ) -> List[Dict[str, Any]]:
        """
        Получает список счетов из банка
        
        Endpoint: GET /accounts?client_id=team200-1
        Headers: Authorization, X-Requesting-Bank, X-Consent-Id
        """
        bank_config = self._get_bank_config(bank_id)
        token = self.get_bank_token(user_id, bank_id)
        
        # Получаем или создаём consent
        consent_key = f"consent:{user_id}:{bank_id}"
        consent_id = self.redis_client.get(consent_key)
        
        if not consent_id:
            consent_id = self.create_consent(
                user_id,
                bank_id,
                client_id,
                ["ReadAccountsDetail", "ReadBalances", "ReadTransactionsDetail"]
            )
        
        url = f"{bank_config['base_url']}/accounts"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Requesting-Bank": bank_config["client_id"],
            "X-Consent-Id": consent_id
        }
        
        params = {
            "client_id": client_id
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Парсим ответ (формат OpenBanking)
                accounts = []
                if "data" in data and "account" in data["data"]:
                    for acc in data["data"]["account"]:
                        accounts.append({
                            "accountId": acc.get("accountId"),
                            "accountName": acc.get("nickname", "Счёт"),
                            "currency": acc.get("currency", "RUB"),
                            "accountType": acc.get("accountType", "Personal")
                        })
                
                logger.info(f"✅ Получено {len(accounts)} счетов из {bank_config['name']}")
                return accounts
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения счетов: {e}")
            # В режиме разработки возвращаем mock данные
            if settings.DEBUG:
                logger.warning(f"⚠️  Используем mock данные для разработки")
                return [
                    {
                        "accountId": f"{bank_config['name']}_acc_001",
                        "accountName": "Основной счёт",
                        "currency": "RUB",
                        "accountType": "Personal"
                    }
                ]
            raise
    
    def get_account_balance(
        self,
        user_id: int,
        bank_id: int,
        account_id: str,
        client_id: str
    ) -> Dict[str, Any]:
        """
        Получает баланс счёта
        
        Endpoint: GET /accounts/{account_id}/balances
        """
        bank_config = self._get_bank_config(bank_id)
        token = self.get_bank_token(user_id, bank_id)
        
        # Получаем consent
        consent_key = f"consent:{user_id}:{bank_id}"
        consent_id = self.redis_client.get(consent_key)
        
        if not consent_id:
            consent_id = self.create_consent(
                user_id,
                bank_id,
                client_id,
                ["ReadAccountsDetail", "ReadBalances"]
            )
        
        url = f"{bank_config['base_url']}/accounts/{account_id}/balances"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Requesting-Bank": bank_config["client_id"],
            "X-Consent-Id": consent_id
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                # Парсим ответ
                if "data" in data and "balance" in data["data"]:
                    balances = data["data"]["balance"]
                    if balances:
                        first_balance = balances[0]
                        return {
                            "amount": float(first_balance.get("amount", {}).get("amount", 0)),
                            "currency": first_balance.get("amount", {}).get("currency", "RUB")
                        }
                
                logger.info(f"✅ Получен баланс для счёта {account_id}")
                return {"amount": 0, "currency": "RUB"}
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения баланса: {e}")
            # Mock данные
            if settings.DEBUG:
                import random
                return {
                    "amount": round(random.uniform(1000, 50000), 2),
                    "currency": "RUB"
                }
            raise
    
    def get_account_transactions(
        self,
        user_id: int,
        bank_id: int,
        account_id: str,
        client_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Получает транзакции по счёту
        
        Endpoint: GET /accounts/{account_id}/transactions
        """
        bank_config = self._get_bank_config(bank_id)
        token = self.get_bank_token(user_id, bank_id)
        
        # Получаем consent
        consent_key = f"consent:{user_id}:{bank_id}"
        consent_id = self.redis_client.get(consent_key)
        
        if not consent_id:
            consent_id = self.create_consent(
                user_id,
                bank_id,
                client_id,
                ["ReadTransactionsDetail"]
            )
        
        url = f"{bank_config['base_url']}/accounts/{account_id}/transactions"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Requesting-Bank": bank_config["client_id"],
            "X-Consent-Id": consent_id
        }
        
        params = {
            "limit": limit
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Парсим ответ
                transactions = []
                if "data" in data and "transaction" in data["data"]:
                    for txn in data["data"]["transaction"]:
                        amount_data = txn.get("amount", {})
                        transactions.append({
                            "id": txn.get("transactionId", ""),
                            "date": txn.get("bookingDateTime", datetime.utcnow().isoformat()),
                            "description": txn.get("transactionInformation", "Транзакция"),
                            "amount": float(amount_data.get("amount", 0)),
                            "currency": amount_data.get("currency", "RUB"),
                            "type": txn.get("creditDebitIndicator", "debit").lower()
                        })
                
                logger.info(f"✅ Получено {len(transactions)} транзакций для {account_id}")
                return transactions
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения транзакций: {e}")
            # Mock данные
            if settings.DEBUG:
                import random
                transactions = []
                for i in range(min(limit, 5)):
                    transactions.append({
                        "id": f"txn_{random.randint(10000, 99999)}",
                        "date": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                        "description": random.choice([
                            "Покупка в магазине",
                            "Оплата ресторана",
                            "Перевод",
                            "Снятие наличных"
                        ]),
                        "amount": round(random.uniform(-500, 1000), 2),
                        "currency": "RUB",
                        "type": "debit" if random.random() > 0.3 else "credit"
                    })
                return transactions
            raise
