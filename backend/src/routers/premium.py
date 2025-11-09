"""
API роутер для Premium подписки
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.dependencies import get_current_user
from src.models.user import User
from src.constants.constants import AccountType
from src.services.payment_service import PaymentService
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/premium", tags=["Premium"])


class PurchasePremiumRequest(BaseModel):
    """Запрос на покупку Premium"""
    from_account_id: int = Field(..., alias='fromAccountId')
    
    class Config:
        populate_by_name = True


@router.post("/purchase", response_model=dict)
async def purchase_premium(
    request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Покупка Premium подписки
    
    Списывает 299₽ с указанного счета и обновляет тариф на Premium.
    Создает транзакцию в истории платежей.
    """
    # Проверяем, не Premium ли уже
    if current_user.account_type == AccountType.PREMIUM:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже активна подписка Premium"
        )
    
    # Получаем account_id из request
    from_account_id = request.get('fromAccountId') or request.get('from_account_id')
    if not from_account_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не указан счет для списания"
        )
    
    # Создаем платеж
    payment, error = PaymentService.create_premium_payment(
        db,
        current_user.id,
        from_account_id,
        amount=299.0
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Обновляем тариф пользователя
    current_user.account_type = AccountType.PREMIUM
    db.commit()
    db.refresh(current_user)
    
    return {
        "success": True,
        "data": {
            "message": "🎉 Поздравляем! Вы перешли на Premium!",
            "accountType": current_user.account_type.value,
            "payment": {
                "id": payment.id,
                "amount": payment.amount,
                "status": payment.status.value,
                "createdAt": payment.created_at.isoformat()
            }
        }
    }


@router.get("/status", response_model=dict)
async def get_premium_status(
    current_user: User = Depends(get_current_user)
):
    """Проверить статус Premium подписки"""
    is_premium = current_user.account_type == AccountType.PREMIUM
    
    return {
        "success": True,
        "data": {
            "isPremium": is_premium,
            "accountType": current_user.account_type.value,
            "features": {
                "maxGroups": 5 if is_premium else 1,
                "maxMembers": 20 if is_premium else 2,
                "unlimitedBanks": is_premium,
                "prioritySupport": is_premium
            }
        }
    }

