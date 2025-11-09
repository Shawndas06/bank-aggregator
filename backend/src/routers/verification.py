"""
API роутер для верификации телефона
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.dependencies import get_current_user
from src.models.user import User
from src.services.otp_service import OTPService
from src.utils.responses import success_response, error_response

router = APIRouter(prefix="/api/verification", tags=["Verification"])

@router.post("/send-phone-code")
async def send_phone_verification_code(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Отправить код подтверждения на телефон"""
    if not current_user.phone:
        return error_response("Номер телефона не указан", 400)
    
    otp_code = OTPService.generate_otp_code(db, current_user.phone)
    
    # В реальности здесь была бы отправка SMS
    # Сейчас просто логируем
    print(f"📱 SMS код для {current_user.phone}: {otp_code}")
    
    return success_response({
        "message": f"Код отправлен на {current_user.phone}",
        "phone": current_user.phone
    })

@router.post("/verify-phone")
async def verify_phone(
    code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Подтвердить номер телефона кодом"""
    if not current_user.phone:
        return error_response("Номер телефона не указан", 400)
    
    is_valid = OTPService.verify_otp_code(db, current_user.phone, code)
    
    if not is_valid:
        return error_response("Неверный код", 400)
    
    # Помечаем телефон как подтвержденный
    # (можно добавить поле phone_verified в модель User)
    
    return success_response({
        "message": "Номер телефона подтвержден",
        "phone": current_user.phone
    })

