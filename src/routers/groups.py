"""
Роутер для работы с группами
РАЗРАБОТЧИКИ: EZIRA (основная логика), BAGA (приглашения)

Эндпоинты:
- POST /api/groups - Создать группу (EZIRA)
- GET /api/groups - Получить список групп (EZIRA)
- GET /api/groups/settings - Получить конфигурацию лимитов (EZIRA)
- POST /api/groups/invite - Отправить приглашение (BAGA)
- POST /api/groups/invite/accept - Принять приглашение (BAGA)
- POST /api/groups/invite/decline - Отклонить приглашение (BAGA)
- GET /api/groups/{id}/accounts - Получить счета группы (EZIRA)
- GET /api/groups/{id}/accounts/{client_id} - Информация по счету (EZIRA)
- GET /api/groups/{id}/accounts/balances - Балансы счетов группы (EZIRA)
- GET /api/groups/{id}/accounts/transactions - Транзакции группы (EZIRA)
- DELETE /api/groups - Удалить группу (EZIRA)
- POST /api/groups/exit - Выйти из группы (EZIRA)
"""
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.dependencies import get_current_verified_user
from src.schemas.group import (
    GroupCreateRequest,
    GroupResponse,
    GroupSettingsResponse,
    InviteRequest,
    InviteActionRequest,
    GroupDeleteRequest,
    GroupExitRequest
)
from src.models.user import User
from src.utils.responses import success_response, error_response

router = APIRouter(prefix="/api/groups", tags=["Groups"])


# ===== EZIRA: Управление группами =====

@router.post("")
async def create_group(
    request: GroupCreateRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Создать новую группу
    
    TODO (EZIRA):
    1. Проверить лимит групп для типа аккаунта пользователя
    2. Создать группу в БД (owner_id = current_user.id)
    3. Автоматически добавить владельца в члены группы
    4. Вернуть данные группы
    """
    # TODO: Implement
    return success_response({
        "id": 1,
        "name": request.name,
        "owner_id": current_user.id
    })


@router.get("")
async def get_groups(
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить список групп пользователя
    
    TODO (EZIRA):
    1. Получить все группы, где пользователь является членом
    2. Вернуть список групп
    """
    # TODO: Implement
    return success_response([])


@router.get("/settings")
async def get_group_settings():
    """
    Получить конфигурацию лимитов для групп
    
    TODO (EZIRA):
    1. Вернуть константы ACCOUNT_LIMITS
    """
    # TODO: Implement
    return success_response({
        "free": {
            "max_groups": 1,
            "max_members": 2
        },
        "premium": {
            "max_groups": 5,
            "max_members": 20
        }
    })


@router.delete("")
async def delete_group(
    request: GroupDeleteRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Удалить группу
    
    TODO (EZIRA):
    1. Проверить, что пользователь является владельцем группы
    2. Удалить все членства в группе
    3. Удалить группу
    4. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "Group deleted successfully"
    })


@router.post("/exit")
async def exit_group(
    request: GroupExitRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Выйти из группы
    
    TODO (EZIRA):
    1. Проверить, что пользователь НЕ является владельцем
    2. Удалить членство пользователя в группе
    3. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "Left group successfully"
    })


@router.get("/{group_id}/accounts")
async def get_group_accounts(
    group_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить список всех счетов членов группы
    
    TODO (EZIRA):
    1. Проверить, что пользователь является членом группы
    2. Получить всех членов группы
    3. Получить все счета членов группы
    4. Вернуть список с информацией о владельцах
    """
    # TODO: Implement
    return success_response([])


@router.get("/{group_id}/accounts/{client_id}")
async def get_group_account_details(
    group_id: int = Path(...),
    client_id: str = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить подробную информацию по конкретному счету в группе
    
    TODO (EZIRA):
    1. Проверить, что пользователь является членом группы
    2. Получить детальную информацию о счете
    3. Вернуть данные счета
    """
    # TODO: Implement
    return success_response({})


@router.get("/{group_id}/accounts/balances")
async def get_group_balances(
    group_id: int = Path(...),
    client_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить балансы всех счетов в группе
    
    TODO (EZIRA):
    1. Проверить, что пользователь является членом группы
    2. Получить балансы всех счетов (или отфильтровать по client_id)
    3. Проверить кеш в Redis
    4. Если кеша нет - получить из API банков
    5. Вернуть список балансов
    """
    # TODO: Implement
    return success_response([])


@router.get("/{group_id}/accounts/transactions")
async def get_group_transactions(
    group_id: int = Path(...),
    client_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Получить транзакции всех счетов в группе
    
    TODO (EZIRA):
    1. Проверить, что пользователь является членом группы
    2. Получить транзакции всех счетов (или отфильтровать по client_id)
    3. Проверить кеш в Redis
    4. Если кеша нет - получить из API банков
    5. Вернуть список транзакций
    """
    # TODO: Implement
    return success_response([])


# ===== BAGA: Приглашения =====

@router.post("/invite")
async def invite_to_group(
    request: InviteRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Отправить приглашение в группу
    
    TODO (BAGA):
    1. Проверить, что пользователь является владельцем или членом группы
    2. Проверить лимит членов группы для типа аккаунта
    3. Проверить, что пользователь с таким email существует
    4. Проверить, что пользователь еще не в группе
    5. Создать приглашение в БД (status=PENDING)
    6. (Опционально) Отправить уведомление на email
    7. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "Invitation sent successfully",
        "request_id": 1
    })


@router.post("/invite/accept")
async def accept_invitation(
    request: InviteActionRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Принять приглашение в группу
    
    TODO (BAGA):
    1. Получить приглашение по request_id
    2. Проверить, что приглашение для current_user (по email)
    3. Проверить, что статус PENDING
    4. Обновить статус на ACCEPTED
    5. Добавить пользователя в члены группы
    6. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "Invitation accepted successfully"
    })


@router.post("/invite/decline")
async def decline_invitation(
    request: InviteActionRequest,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Отклонить приглашение в группу
    
    TODO (BAGA):
    1. Получить приглашение по request_id
    2. Проверить, что приглашение для current_user (по email)
    3. Проверить, что статус PENDING
    4. Обновить статус на DECLINED
    5. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "Invitation declined"
    })


