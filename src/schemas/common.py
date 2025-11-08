"""
Общие схемы для API ответов
"""
from pydantic import BaseModel
from typing import Any, Optional, Dict


class SuccessResponse(BaseModel):
    """Схема успешного ответа"""
    success: bool = True
    data: Any


class ErrorDetail(BaseModel):
    """Детали ошибки"""
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Схема ответа с ошибкой"""
    success: bool = False
    error: ErrorDetail


