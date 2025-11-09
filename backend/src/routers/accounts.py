import logging
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import redis

from src.database import get_db
from src.redis_client import get_redis
from src.dependencies import get_current_verified_user
from src.schemas.account import (
    AccountAttachRequest,
    AccountCreateRequest,
    AccountResponse,
    BalanceResponse,
    TransactionResponse
)
from src.schemas.profile import AccountRenameRequest
from src.models.user import User
from src.services.account_service import AccountService
from src.utils.responses import success_response, error_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])

@router.post("/attach")
async def attach_account(
    request: AccountAttachRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)

    success, error = service.attach_account(current_user.id, request.id)

    if not success:
        return error_response(error, 400)

    return success_response({
        "message": "Счёт успешно привязан",
        "accountId": request.id
    })

@router.get("")
async def get_accounts(
    client_id: Optional[int] = Query(None, description="ID банка для фильтрации"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)

    accounts = service.get_user_accounts(current_user.id, client_id)

    return success_response(accounts)

@router.post("")
async def create_account(
    request: AccountCreateRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)

    account, error = service.create_account(
        current_user.id,
        request.client_id,
        None
    )

    if error:
        return error_response(error, 400)

    return success_response({
        "message": "Счёт успешно создан",
        "account": {
            "accountId": account.account_id,
            "accountName": account.account_name,
            "clientId": account.bank_id,
            "isActive": account.is_active
        }
    }, 201)

@router.get("/{account_id}")
async def get_account(
    account_id: str,
    client_id: int = Query(..., description="ID банка"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)

    account_info = service.get_account_info(current_user.id, account_id, client_id)

    if not account_info:
        return error_response("Счёт не найден", 404)

    return success_response(account_info)

@router.get("/{account_id}/balances")
async def get_account_balances(
    account_id: str,
    client_id: int = Query(..., description="ID банка"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)

    balance = service.get_account_balance(current_user.id, account_id, client_id)

    if not balance:
        return error_response("Не удалось получить баланс", 404)

    return success_response(balance)

@router.get("/{account_id}/transactions")
async def get_account_transactions(
    account_id: str,
    client_id: int = Query(..., description="ID банка"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)

    transactions = service.get_account_transactions(current_user.id, account_id, client_id)

    return success_response(transactions)

@router.get("/balances/all")
async def get_all_balances(
    client_ids: Optional[str] = Query(None, description="ID банков через запятую (1,2,3)"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)

    bank_ids = None
    if client_ids:
        try:
            bank_ids = [int(x.strip()) for x in client_ids.split(',')]
        except ValueError:
            return error_response("Неверный формат client_ids. Используйте: 1,2,3", 400)

    balances = service.get_all_user_balances(current_user.id, bank_ids)

    return success_response(balances)

@router.get("/transactions/all")
async def get_all_transactions(
    client_ids: Optional[str] = Query(None, description="ID банков через запятую (1,2,3)"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(20, ge=1, le=100, description="Количество записей (max 100)"),
    start_date: Optional[str] = Query(None, description="Дата начала (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Дата окончания (YYYY-MM-DD)"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)

    bank_ids = None
    if client_ids:
        try:
            bank_ids = [int(x.strip()) for x in client_ids.split(',')]
        except ValueError:
            return error_response("Неверный формат client_ids. Используйте: 1,2,3", 400)

    transactions = service.get_all_user_transactions(
        current_user.id,
        bank_ids,
        offset,
        limit,
        start_date,
        end_date
    )

    return success_response(transactions)

@router.put("/{account_id}/rename")
async def rename_account(
    account_id: int,
    request: AccountRenameRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)
    
    success, error = service.rename_account(current_user.id, account_id, request.account_name)
    
    if not success:
        return error_response(error, 404)
    
    return success_response({
        "message": "Счёт успешно переименован",
        "accountId": account_id,
        "newName": request.account_name
    })

@router.post("/{account_id}/sync")
async def force_sync_account(
    account_id: int,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    redis_client = get_redis()
    service = AccountService(db, redis_client)
    
    sync_result, error = service.force_sync_account(current_user.id, account_id)
    
    if error:
        return error_response(error, 400)
    
    return success_response({
        "message": "Счёт успешно синхронизирован",
        "syncData": sync_result
    })
