"""
Стандартизированные ответы API
"""
from typing import Any, Optional, Dict
from fastapi.responses import JSONResponse


def success_response(data: Any = None, status_code: int = 200) -> JSONResponse:
    """
    Формирует успешный ответ API.
    
    Args:
        data: Данные для ответа
        status_code: HTTP статус код (по умолчанию 200)
    
    Returns:
        JSONResponse: Стандартизированный ответ
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": data
        }
    )


def error_response(
    message: str,
    status_code: int = 400,
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Формирует ответ с ошибкой.
    
    Args:
        message: Сообщение об ошибке
        status_code: HTTP статус код (по умолчанию 400)
        details: Дополнительные детали ошибки
    
    Returns:
        JSONResponse: Стандартизированный ответ с ошибкой
    """
    error_content = {"message": message}
    if details:
        error_content["details"] = details
    
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": error_content
        }
    )


