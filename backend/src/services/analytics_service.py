import logging
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, timedelta
import redis

from src.services.account_service import AccountService
from src.constants.mcc_mapping import categorize_transaction, CATEGORY_NAMES_RU
from src.constants.constants import TransactionCategory

logger = logging.getLogger(__name__)

class AnalyticsService:
    
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client
        self.account_service = AccountService(db, redis_client)
    
    def get_user_overview(
        self,
        user_id: int,
        bank_ids: List[int] = None
    ) -> Dict[str, Any]:
        """
        Обзорная аналитика пользователя: балансы, доходы, расходы
        """
        accounts = self.account_service.get_user_accounts(user_id, None)
        
        if bank_ids:
            accounts = [acc for acc in accounts if acc["clientId"] in bank_ids]
        
        total_balance = 0.0
        balances_by_currency = {}
        
        for account in accounts:
            try:
                balance = self.account_service.get_account_balance(
                    user_id,
                    account["accountId"],
                    account["clientId"]
                )
                
                amount = balance.get("amount", 0)
                currency = balance.get("currency", "RUB")
                
                total_balance += amount
                
                if currency not in balances_by_currency:
                    balances_by_currency[currency] = 0
                balances_by_currency[currency] += amount
                
            except Exception as e:
                logger.error(f"Ошибка получения баланса: {e}")
                continue
        
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        previous_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        
        current_expenses = 0.0
        current_income = 0.0
        previous_expenses = 0.0
        previous_income = 0.0
        
        category_totals = {}
        
        for account in accounts:
            try:
                transactions = self.account_service.get_account_transactions(
                    user_id,
                    account["accountId"],
                    account["clientId"]
                )
                
                for txn in transactions:
                    try:
                        txn_date = datetime.fromisoformat(txn["date"].replace('Z', '+00:00'))
                        amount = abs(txn["amount"])
                        txn_type = txn.get("type", "debit")
                        
                        category = categorize_transaction(
                            txn.get("mccCode", ""),
                            txn.get("description", "")
                        )
                        
                        if txn_date >= current_month_start:
                            if txn_type == "debit":
                                current_expenses += amount
                                
                                if category not in category_totals:
                                    category_totals[category] = 0
                                category_totals[category] += amount
                            else:
                                current_income += amount
                        
                        elif txn_date >= previous_month_start and txn_date < current_month_start:
                            if txn_type == "debit":
                                previous_expenses += amount
                            else:
                                previous_income += amount
                    
                    except Exception as e:
                        logger.warning(f"Ошибка обработки транзакции: {e}")
                        continue
                
            except Exception as e:
                logger.error(f"Ошибка получения транзакций: {e}")
                continue
        
        top_categories = sorted(
            [
                {
                    "category": cat.value,
                    "categoryName": CATEGORY_NAMES_RU.get(cat, cat.value),
                    "amount": amount,
                    "percentage": round((amount / current_expenses * 100) if current_expenses > 0 else 0, 1)
                }
                for cat, amount in category_totals.items()
            ],
            key=lambda x: x["amount"],
            reverse=True
        )[:5]
        
        expense_change = 0.0
        if previous_expenses > 0:
            expense_change = round(((current_expenses - previous_expenses) / previous_expenses) * 100, 1)
        
        income_change = 0.0
        if previous_income > 0:
            income_change = round(((current_income - previous_income) / previous_income) * 100, 1)
        
        return {
            "totalBalance": total_balance,
            "balanceByCurrency": balances_by_currency,
            "currentMonth": {
                "expenses": current_expenses,
                "income": current_income,
                "expenseChange": expense_change,
                "incomeChange": income_change
            },
            "topCategories": top_categories,
            "accountsCount": len(accounts)
        }
    
    def get_categories_breakdown(
        self,
        user_id: int,
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict[str, Any]]:
        """
        Детальная разбивка расходов по категориям
        """
        accounts = self.account_service.get_user_accounts(user_id, None)
        
        category_data = {}
        
        for account in accounts:
            try:
                transactions = self.account_service.get_account_transactions(
                    user_id,
                    account["accountId"],
                    account["clientId"]
                )
                
                for txn in transactions:
                    try:
                        txn_date = datetime.fromisoformat(txn["date"].replace('Z', '+00:00'))
                        
                        if start_date:
                            start = datetime.fromisoformat(start_date)
                            if txn_date < start:
                                continue
                        
                        if end_date:
                            end = datetime.fromisoformat(end_date)
                            if txn_date > end:
                                continue
                        
                        if txn.get("type") == "debit":
                            category = categorize_transaction(
                                txn.get("mccCode", ""),
                                txn.get("description", "")
                            )
                            
                            if category not in category_data:
                                category_data[category] = {
                                    "amount": 0,
                                    "count": 0,
                                    "transactions": []
                                }
                            
                            category_data[category]["amount"] += abs(txn["amount"])
                            category_data[category]["count"] += 1
                            category_data[category]["transactions"].append({
                                "id": txn["id"],
                                "date": txn["date"],
                                "description": txn["description"],
                                "amount": abs(txn["amount"])
                            })
                    
                    except Exception as e:
                        logger.warning(f"Ошибка обработки транзакции: {e}")
                        continue
            
            except Exception as e:
                logger.error(f"Ошибка получения транзакций: {e}")
                continue
        
        total_amount = sum(data["amount"] for data in category_data.values())
        
        result = []
        for category, data in category_data.items():
            result.append({
                "category": category.value,
                "categoryName": CATEGORY_NAMES_RU.get(category, category.value),
                "amount": data["amount"],
                "count": data["count"],
                "percentage": round((data["amount"] / total_amount * 100) if total_amount > 0 else 0, 1),
                "topTransactions": sorted(data["transactions"], key=lambda x: x["amount"], reverse=True)[:5]
            })
        
        return sorted(result, key=lambda x: x["amount"], reverse=True)

