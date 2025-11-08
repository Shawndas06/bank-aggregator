"""
Роутер для аутентификации и авторизации
РАЗРАБОТЧИК: BAGA

Эндпоинты:
- POST /api/auth/sign-up - Регистрация пользователя
- POST /api/auth/verify-email - Подтверждение email (OTP)
- POST /api/auth/sign-in - Вход пользователя
- GET /api/auth/me - Получение информации о текущем пользователе
- POST /api/auth/logout - Выход пользователя
"""
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.database import get_db
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
from src.utils.responses import success_response, error_response

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/sign-up")
async def sign_up(
    request: SignUpRequest,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя
    
    TODO (BAGA):
    1. Проверить, что email не занят
    2. Валидировать пароль (минимум 8 символов, заглавные, строчные, цифры)
    3. Проверить возраст (18+)
    4. Захешировать пароль
    5. Создать пользователя (is_verified=False)
    6. Сгенерировать OTP код и сохранить в Redis с ttl
    7. (Опционально) Отправить OTP на email
    8. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "User registered. Please verify your email.",
        "email": request.email
    })


@router.post("/verify-email")
async def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    """
    Подтверждение email через OTP код
    
    TODO (BAGA):
    1. Получить OTP из Redis по email
    2. Проверить, что код совпадает
    3. Обновить is_verified=True для пользователя
    4. Удалить OTP из Redis
    5. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "Email verified successfully"
    })


@router.post("/sign-in")
async def sign_in(
    request: SignInRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Вход пользователя
    
    TODO (BAGA):
    1. Найти пользователя по email
    2. Проверить пароль
    3. Проверить, что аккаунт подтвержден (is_verified=True)
    4. Создать сессию (session_id) в Redis с ttl 24 часа
    5. Установить session-id в httponly cookie
    6. Вернуть данные пользователя
    """
    # TODO: Implement
    return success_response({
        "message": "Logged in successfully",
        "user": {
            "id": 1,
            "name": "Test User",
            "birth_date": "2000-01-01",
            "account_type": "free"
        }
    })


@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_verified_user)
):
    """
    Получение информации о текущем пользователе
    
    TODO (BAGA):
    1. Вернуть данные текущего пользователя (из dependency)
    """
    # TODO: Implement
    return success_response({
        "id": current_user.id,
        "name": current_user.name,
        "birth_date": str(current_user.birth_date),
        "account_type": current_user.account_type
    })


@router.post("/logout")
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """
    Выход пользователя
    
    TODO (BAGA):
    1. Получить session-id из cookie
    2. Удалить сессию из Redis
    3. Очистить cookie
    4. Вернуть успешный ответ
    """
    # TODO: Implement
    return success_response({
        "message": "Logged out successfully"
    })


