import logging
import json
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional, Tuple
import redis

from src.models.account import BankAccount
from src.models.user import User
from src.services.bank_client import BankClient
from src.config import settings

logger = logging.getLogger(__name__)

class AccountService:

    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client
        self.bank_client = BankClient(redis_client)

    def get_user_accounts(
        self,
        user_id: int,
        bank_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        query = self.db.query(BankAccount).filter(BankAccount.user_id == user_id)

        if bank_id:
            query = query.filter(BankAccount.bank_id == bank_id)

        accounts = query.all()

        result = []
        for acc in accounts:
            result.append({
                "accountId": acc.account_id,
                "accountName": acc.account_name,
                "clientId": acc.bank_id,
                "clientName": self._get_bank_name(acc.bank_id),
                "isActive": acc.is_active
            })

        return result

    def create_account(
        self,
        user_id: int,
        bank_id: int,
        account_name: Optional[str] = None
    ) -> Tuple[Optional[BankAccount], Optional[str]]:
        try:
            client_id = f"{settings.TEAM_CLIENT_ID}-{user_id}"

            consent_id = self.bank_client.create_consent(
                user_id,
                bank_id,
                client_id,
                ["ReadAccountsDetail", "ReadBalances", "ReadTransactionsDetail"]
            )

            bank_accounts = self.bank_client.get_accounts(user_id, bank_id, client_id)

            if not bank_accounts:
                return None, "Не удалось получить счета из банка"

            first_acc = bank_accounts[0]

            new_account = BankAccount(
                user_id=user_id,
                bank_id=bank_id,
                account_id=first_acc["accountId"],
                account_name=account_name or first_acc.get("accountName", "Счёт"),
                consent_id=consent_id,
                is_active=True
            )

            self.db.add(new_account)
            self.db.commit()
            self.db.refresh(new_account)

            logger.info(f"✅ Создан счёт {new_account.id} для пользователя {user_id}")
            return new_account, None

        except Exception as e:
            logger.error(f"❌ Ошибка создания счёта: {e}")
            return None, str(e)

    def attach_account(
        self,
        user_id: int,
        account_id: int
    ) -> Tuple[bool, Optional[str]]:
        account = self.db.query(BankAccount).filter(BankAccount.id == account_id).first()

        if not account:
            return False, "Счёт не найден"

        if account.user_id and account.user_id != user_id:
            return False, "Счёт уже привязан к другому пользователю"

        account.user_id = user_id
        account.is_active = True
        self.db.commit()

        logger.info(f"✅ Счёт {account_id} привязан к пользователю {user_id}")
        return True, None

    def get_account_info(
        self,
        user_id: int,
        account_id: str,
        bank_id: int
    ) -> Optional[Dict[str, Any]]:
        cache_key = f"account_info:{user_id}:{account_id}"

        cached = self.redis_client.get(cache_key)
        if cached:
            logger.info(f"✅ Используем кешированную информацию о счёте {account_id}")
            return json.loads(cached)

        account = (
            self.db.query(BankAccount)
            .filter(
                BankAccount.user_id == user_id,
                BankAccount.account_id == account_id,
                BankAccount.bank_id == bank_id
            )
            .first()
        )

        if not account:
            return None

        info = {
            "accountId": account.account_id,
            "accountName": account.account_name,
            "clientId": account.bank_id,
            "clientName": self._get_bank_name(account.bank_id),
            "isActive": account.is_active
        }

        self.redis_client.setex(
            cache_key,
            settings.BANK_DATA_CACHE_TTL,
            json.dumps(info)
        )

        return info

    def get_account_balance(
        self,
        user_id: int,
        account_id: str,
        bank_id: int
    ) -> Optional[Dict[str, Any]]:
        cache_key = f"balance:{user_id}:{account_id}"

        cached = self.redis_client.get(cache_key)
        if cached:
            logger.info(f"✅ Используем кешированный баланс для {account_id}")
            return json.loads(cached)

        client_id = f"{settings.TEAM_CLIENT_ID}-{user_id}"
        balance = self.bank_client.get_account_balance(user_id, bank_id, account_id, client_id)

        self.redis_client.setex(
            cache_key,
            settings.BANK_DATA_CACHE_TTL,
            json.dumps(balance)
        )

        return balance

    def get_account_transactions(
        self,
        user_id: int,
        account_id: str,
        bank_id: int
    ) -> List[Dict[str, Any]]:
        cache_key = f"transactions:{user_id}:{account_id}"

        cached = self.redis_client.get(cache_key)
        if cached:
            logger.info(f"✅ Используем кешированные транзакции для {account_id}")
            return json.loads(cached)

        client_id = f"{settings.TEAM_CLIENT_ID}-{user_id}"
        transactions = self.bank_client.get_account_transactions(
            user_id,
            bank_id,
            account_id,
            client_id
        )

        self.redis_client.setex(
            cache_key,
            settings.BANK_DATA_CACHE_TTL,
            json.dumps(transactions)
        )

        return transactions

    def _get_bank_name(self, bank_id: int) -> str:
        bank_names = {
            1: "vbank",
            2: "sbank",
            3: "abank"
        }
        return bank_names.get(bank_id, f"bank{bank_id}")
