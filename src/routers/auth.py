"""
Роутер для аутентификации и авторизации
"""
import logging
from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.redis_client import get_redis
from src.dependencies import get_current_user, get_current_verified_user
from src.schemas.auth import (
    SignUpRequest,
    SignUpResponse,
    VerifyEmailRequest,
    SignInRequest,
    SignInResponse,
    UserResponse
)
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.session_service import SessionService
from src.services.otp_service import OTPService
from src.utils.responses import success_response, error_response
from src.config import settings
import redis

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/sign-up")
async def sign_up(
    request: SignUpRequest,
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя"""
    # Создаём пользователя
    user, error = AuthService.create_user(
        db,
        request.email,
        request.password,
        request.name,
        request.birth_date
    )
    
    if error:
        return error_response(error, 400)
    
    # Генерируем OTP код
    otp_code = OTPService.generate_otp_code(db, user.email)
    OTPService.send_otp_email(user.email, otp_code)
    
    return success_response({
        "message": "Регистрация успешна! Проверьте email для подтверждения.",
        "email": user.email,
        "otpCode": otp_code if settings.DEBUG else None  # Только для разработки
    }, 201)


@router.post("/verify-email")
async def verify_email(
    request: VerifyEmailRequest,
    response: Response,
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis)
):
    """Подтверждение email через OTP код"""
    # Проверяем OTP
    is_valid, error = OTPService.verify_otp(db, request.email, request.code)
    
    if not is_valid:
        return error_response(error, 400)
    
    # Подтверждаем пользователя
    user = AuthService.verify_user(db, request.email)
    if not user:
        return error_response("Пользователь не найден", 404)
    
    # Создаём сессию и автоматически логиним
    session_id = SessionService.create_session(redis_client, user.id)
    
    # Создаём ответ
    json_response = success_response({
        "message": "Email подтверждён! Вы автоматически вошли в систему.",
        "user": {
            "id": user.id,
            "name": user.name,
            "birthDate": str(user.birth_date),
            "accountType": user.account_type.value
        }
    })
    
    # Устанавливаем cookie в response
    json_response.set_cookie(
        key="session-id",
        value=session_id,
        max_age=settings.SESSION_EXPIRE_HOURS * 3600,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax"
    )
    
    return json_response


@router.post("/sign-in")
async def sign_in(
    request: SignInRequest,
    response: Response,
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis)
):
    """Вход в систему"""
    # Аутентификация
    user, error = AuthService.authenticate_user(db, request.email, request.password)
    
    if error:
        return error_response(error, 401)
    
    # Создаём сессию
    session_id = SessionService.create_session(redis_client, user.id)
    
    # Создаём ответ
    json_response = success_response({
        "message": "Вход выполнен успешно",
        "user": {
            "id": user.id,
            "name": user.name,
            "birthDate": str(user.birth_date),
            "accountType": user.account_type.value
        }
    })
    
    # Устанавливаем cookie
    json_response.set_cookie(
        key="session-id",
        value=session_id,
        max_age=settings.SESSION_EXPIRE_HOURS * 3600,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax"
    )
    
    return json_response


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_verified_user)):
    """Получить данные текущего пользователя"""
    return success_response({
        "id": current_user.id,
        "name": current_user.name,
        "birthDate": str(current_user.birth_date),
        "accountType": current_user.account_type.value
    })


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    redis_client: redis.Redis = Depends(get_redis)
):
    """Выход из системы"""
    session_id = request.cookies.get("session-id")
    
    if session_id:
        SessionService.delete_session(redis_client, session_id)
    
    # Создаём ответ
    json_response = success_response({
        "message": "Выход выполнен успешно"
    })
    
    # Удаляем cookie
    json_response.delete_cookie("session-id")
    
    return json_response
