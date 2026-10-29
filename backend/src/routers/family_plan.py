"""
API роутер для семейного финансового плана.

Все эндпоинты требуют аутентификации и членства в группе.
Серверная проверка: /api/family-plan/{group_id}/* доступен
только участникам группы group_id.
"""
import logging
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import get_current_verified_user
from src.models.user import User
from src.services.family_plan_service import FamilyPlanService
from src.schemas.family_plan import (
    ObligationCreate, ObligationUpdate,
    ContributionCreate, SharedResourceCreate,
)
from src.utils.responses import success_response, error_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/family-plan", tags=["Family Plan"])


# ─── Обязательства ────────────────────────────────────────────────────────────

@router.post("/{group_id}/obligations")
async def create_obligation(
    data: ObligationCreate,
    group_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Создать обязательный платёж в плане группы."""
    obligation, error = FamilyPlanService.create_obligation(
        db=db,
        group_id=group_id,
        creator_id=current_user.id,
        name=data.name,
        amount_rub=data.amount_rub,
        due_date=data.due_date,
        responsible_user_id=data.responsible_user_id,
        description=data.description,
        is_recurring=data.is_recurring,
        recurring_day=data.recurring_day,
    )
    if error:
        return error_response(error, 400)

    return success_response(_serialize_obligation(obligation), 201)


@router.get("/{group_id}/obligations")
async def list_obligations(
    group_id: int = Path(...),
    include_paid: bool = Query(False),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Получить список обязательств группы."""
    obligations, error = FamilyPlanService.list_obligations(
        db, group_id, current_user.id, include_paid
    )
    if error:
        return error_response(error, 403)

    return success_response([_serialize_obligation(o) for o in obligations])


@router.post("/{group_id}/obligations/{obligation_id}/pay")
async def mark_obligation_paid(
    group_id: int = Path(...),
    obligation_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Отметить обязательство как оплаченное."""
    ok, error = FamilyPlanService.mark_paid(db, obligation_id, current_user.id)
    if not ok:
        return error_response(error, 400)
    return success_response({"message": "Обязательство отмечено как оплаченное ✅"})


@router.delete("/{group_id}/obligations/{obligation_id}")
async def delete_obligation(
    group_id: int = Path(...),
    obligation_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Удалить обязательство."""
    ok, error = FamilyPlanService.delete_obligation(db, obligation_id, current_user.id)
    if not ok:
        return error_response(error, 400)
    return success_response({"message": "Обязательство удалено"})


# ─── Взносы ───────────────────────────────────────────────────────────────────

@router.post("/{group_id}/contributions")
async def create_contribution(
    data: ContributionCreate,
    group_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Предложить взнос в план группы."""
    contribution, error = FamilyPlanService.create_contribution(
        db=db,
        group_id=group_id,
        contributor_id=current_user.id,
        amount_rub=data.amount_rub,
        expected_date=data.expected_date,
        note=data.note,
    )
    if error:
        return error_response(error, 400)

    return success_response(_serialize_contribution(contribution), 201)


@router.get("/{group_id}/contributions")
async def list_contributions(
    group_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Получить список взносов группы."""
    contributions, error = FamilyPlanService.list_contributions(db, group_id, current_user.id)
    if error:
        return error_response(error, 403)

    return success_response([_serialize_contribution(c) for c in contributions])


@router.post("/{group_id}/contributions/{contribution_id}/confirm")
async def confirm_contribution(
    group_id: int = Path(...),
    contribution_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Подтвердить взнос другого участника."""
    ok, error = FamilyPlanService.confirm_contribution(db, contribution_id, current_user.id)
    if not ok:
        return error_response(error, 400)
    return success_response({"message": "Взнос подтверждён ✅"})


@router.post("/{group_id}/contributions/{contribution_id}/cancel")
async def cancel_contribution(
    group_id: int = Path(...),
    contribution_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Отменить взнос."""
    ok, error = FamilyPlanService.cancel_contribution(db, contribution_id, current_user.id)
    if not ok:
        return error_response(error, 400)
    return success_response({"message": "Взнос отменён"})


@router.post("/{group_id}/contributions/{contribution_id}/receive")
async def mark_contribution_received(
    group_id: int = Path(...),
    contribution_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """Отметить взнос как фактически полученный."""
    ok, error = FamilyPlanService.mark_received(db, contribution_id, current_user.id)
    if not ok:
        return error_response(error, 400)
    return success_response({"message": "Взнос отмечен как полученный ✅"})


# ─── Общие ресурсы ────────────────────────────────────────────────────────────

@router.post("/{group_id}/resources")
async def set_shared_resource(
    data: SharedResourceCreate,
    group_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """
    Включить счёт или объявить фиксированный взнос в семейный план.

    Приглашение само по себе не раскрывает счета.
    Только явное включение через этот эндпоинт открывает доступ партнёру.
    """
    resource, error = FamilyPlanService.set_shared_resource(
        db=db,
        group_id=group_id,
        user_id=current_user.id,
        resource_type=data.resource_type,
        bank_client_id=data.bank_client_id,
        bank_account_id=data.bank_account_id,
        fixed_amount_kopecks=data.fixed_amount_kopecks,
        visibility=data.visibility,
    )
    if error:
        return error_response(error, 400)

    return success_response(_serialize_resource(resource), 201)


@router.get("/{group_id}/resources")
async def get_shared_resources(
    group_id: int = Path(...),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """
    Получить список включённых ресурсов группы.

    Возвращает только явно разрешённые ресурсы.
    Транзакции личных счётов НЕ раскрываются — только баланс.
    """
    resources, error = FamilyPlanService.get_shared_resources(db, group_id, current_user.id)
    if error:
        return error_response(error, 403)

    return success_response([_serialize_resource(r) for r in resources])


# ─── Прогноз ──────────────────────────────────────────────────────────────────

@router.get("/{group_id}/forecast")
async def get_forecast(
    group_id: int = Path(...),
    included_balance_rub: float = Query(..., description="Текущий баланс включённых счетов (₽)"),
    reserve_rub: float = Query(5000.0, description="Резерв на бытовые расходы (₽)"),
    days_ahead: int = Query(30, ge=7, le=90),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db),
):
    """
    Прогноз денежного потока семейного плана на N дней.

    included_balance_rub — текущий суммарный баланс включённых счетов.
    Передаётся фронтендом (получен из банковского API).
    Сервер не хранит балансы — только план.
    """
    result = FamilyPlanService.calculate_forecast(
        db=db,
        group_id=group_id,
        requester_id=current_user.id,
        included_balance_rub=included_balance_rub,
        reserve_rub=reserve_rub,
        days_ahead=days_ahead,
    )
    if "error" in result:
        return error_response(result["error"], 403)

    return success_response(result)


# ─── Сериализаторы ────────────────────────────────────────────────────────────

def _serialize_obligation(o) -> dict:
    return {
        "id": o.id,
        "groupId": o.group_id,
        "name": o.name,
        "description": o.description,
        "amountRub": o.amount_rub,
        "dueDate": o.due_date.isoformat(),
        "isRecurring": o.is_recurring,
        "recurringDay": o.recurring_day,
        "responsibleUserId": o.responsible_user_id,
        "responsibleUserName": o.responsible_user.name if o.responsible_user else "—",
        "status": o.status.value,
        "paidAt": o.paid_at.isoformat() if o.paid_at else None,
        "createdBy": o.created_by,
        "createdAt": o.created_at.isoformat(),
    }


def _serialize_contribution(c) -> dict:
    return {
        "id": c.id,
        "groupId": c.group_id,
        "contributorUserId": c.contributor_user_id,
        "contributorName": c.contributor.name if c.contributor else "—",
        "amountRub": c.amount_rub,
        "expectedDate": c.expected_date.isoformat(),
        "note": c.note,
        "status": c.status.value,
        "confirmedBy": c.confirmed_by,
        "confirmedByName": c.confirmer.name if c.confirmer else None,
        "received": c.received,
        "receivedAt": c.received_at.isoformat() if c.received_at else None,
        "createdAt": c.created_at.isoformat(),
    }


def _serialize_resource(r) -> dict:
    return {
        "id": r.id,
        "userId": r.user_id,
        "userName": r.user.name if r.user else "—",
        "resourceType": r.resource_type,
        "bankClientId": r.bank_client_id,
        "bankAccountId": r.bank_account_id,
        "fixedAmountRub": r.fixed_amount_kopecks / 100.0 if r.fixed_amount_kopecks else None,
        "visibility": r.visibility,
        "isActive": r.is_active,
    }
