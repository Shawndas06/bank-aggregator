"""
Схемы для групп
РАЗРАБОТЧИКИ: EZIRA (основная логика), BAGA (приглашения)
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class GroupCreateRequest(BaseModel):
    """Запрос на создание группы"""
    name: str


class GroupResponse(BaseModel):
    """Информация о группе"""
    id: int
    name: str
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class GroupListResponse(BaseModel):
    """Список групп"""
    groups: List[GroupResponse]


class GroupSettingsResponse(BaseModel):
    """Настройки лимитов для групп"""
    free: dict
    premium: dict


class InviteRequest(BaseModel):
    """Запрос на приглашение в группу"""
    group_id: int
    email: EmailStr


class InviteActionRequest(BaseModel):
    """Запрос на принятие/отклонение приглашения"""
    request_id: int


class GroupMemberResponse(BaseModel):
    """Информация о члене группы"""
    user_id: int
    name: str
    email: str
    joined_at: datetime


class GroupAccountOwnerResponse(BaseModel):
    """Владелец счета в группе"""
    name: str


class GroupAccountResponse(BaseModel):
    """Счет в группе"""
    owner: GroupAccountOwnerResponse
    client_id: str
    client_name: str


class GroupExitRequest(BaseModel):
    """Запрос на выход из группы"""
    group_id: int


class GroupDeleteRequest(BaseModel):
    """Запрос на удаление группы"""
    group_id: int


