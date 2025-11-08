"""
Роутер для работы с банковскими счетами
РАЗРАБОТЧИК: EZIRA

Эндпоинты:
- POST /api/accounts/attach - Привязать счет к аккаунту
- GET /api/accounts - Получить список всех счетов пользователя
- POST /api/accounts - Создать счет
- GET /api/accounts/{account_id} - Получить информацию по счету
- GET /api/accounts/{account_id}/balances - Получить баланс по счету
- GET /api/accounts/{account_id}/transactions - Получить транзакции по счету
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.dependencies import get_current_verified_user
from src.schemas.account import (
    AccountAttachRequest,
    AccountCreateRequest,
    AccountResponse,
    BalanceResponse,
    TransactionResponse
)
from src.models.user import User
from src.utils.responses import success_response, error_response

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.post("/attach")
async def attach_account(
    request: AccountAttachRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Привязать счет к аккаунту пользователя
    
    TODO (EZIRA):
    1. Проверить, что счет существует
    2. Проверить, что счет не привязан к другому пользователю
    3. Привязать счет к current_user
    4. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "Account attached successfully",
        "account_id": request.id
    })


@router.get("")
async def get_accounts(
    client_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить список счетов
    
    TODO (EZIRA):
    1. Если client_id указан - фильтровать по банку
    2. Получить все счета пользователя из БД
    3. Вернуть список счетов
    """
    # TODO: Implement
    return success_response([])


@router.post("")
async def create_account(
    request: AccountCreateRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Создать новый счет
    
    TODO (EZIRA):
    1. Получить токен банка из Redis (или создать новый)
    2. Создать consent через bank_client
    3. Создать счет через API банка
    4. Сохранить информацию о счете в БД
    5. Вернуть данные счета
    """
    # TODO: Implement
    return success_response({
        "message": "Account created successfully",
        "account_id": "123"
    })


@router.get("/{account_id}")
async def get_account(
    account_id: int,
    client_id: int = Query(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить информацию по счету
    
    TODO (EZIRA):
    1. Проверить, что счет принадлежит пользователю
    2. Проверить кеш в Redis
    3. Если кеша нет - получить данные из API банка
    4. Сохранить в кеш с ttl 4 часа
    5. Вернуть данные счета
    """
    # TODO: Implement
    return success_response({
        "account_id": str(account_id),
        "client_id": client_id,
        "client_name": "vbank",
        "account_name": "Main Account",
        "is_active": True
    })


@router.get("/{account_id}/balances")
async def get_account_balances(
    account_id: int,
    client_id: int = Query(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить баланс по счету
    
    TODO (EZIRA):
    1. Проверить, что счет принадлежит пользователю
    2. Проверить кеш в Redis
    3. Если кеша нет - получить баланс из API банка
    4. Сохранить в кеш с ttl 4 часа
    5. Вернуть баланс
    """
    # TODO: Implement
    return success_response({
        "amount": 1200.50,
        "currency": "EUR"
    })


@router.get("/{account_id}/transactions")
async def get_account_transactions(
    account_id: int,
    client_id: int = Query(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить транзакции по счету
    
    TODO (EZIRA):
    1. Проверить, что счет принадлежит пользователю
    2. Проверить кеш в Redis
    3. Если кеша нет - получить транзакции из API банка
    4. Сохранить в кеш с ttl 4 часа
    5. Вернуть список транзакций
    """
    # TODO: Implement
    return success_response([])
