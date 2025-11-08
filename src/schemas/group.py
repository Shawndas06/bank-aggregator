"""
Схемы для групп
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class GroupCreateRequest(BaseModel):
    """Запрос на создание группы"""
    name: str


class GroupResponse(BaseModel):
    """Информация о группе"""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    id: int
    name: str
    owner_id: int = Field(..., serialization_alias='ownerId')
    created_at: datetime = Field(..., serialization_alias='createdAt')


class GroupListResponse(BaseModel):
    """Список групп"""
    groups: List[GroupResponse]


class GroupSettingsResponse(BaseModel):
    """Настройки лимитов для групп"""
    free: dict
    premium: dict


class InviteRequest(BaseModel):
    """Запрос на приглашение в группу"""
    model_config = ConfigDict(populate_by_name=True)
    
    group_id: int = Field(..., alias='groupId')
    email: EmailStr


class InviteActionRequest(BaseModel):
    """Запрос на принятие/отклонение приглашения"""
    model_config = ConfigDict(populate_by_name=True)
    
    request_id: int = Field(..., alias='requestId')


class GroupMemberResponse(BaseModel):
    """Информация о члене группы"""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    user_id: int = Field(..., serialization_alias='userId')
    name: str
    email: str
    joined_at: datetime = Field(..., serialization_alias='joinedAt')


class GroupAccountOwnerResponse(BaseModel):
    """Владелец счета в группе"""
    name: str


class GroupAccountResponse(BaseModel):
    """Счет в группе"""
    owner: GroupAccountOwnerResponse
    client_id: str = Field(..., serialization_alias='clientId')
    client_name: str = Field(..., serialization_alias='clientName')


class GroupExitRequest(BaseModel):
    """Запрос на выход из группы"""
    model_config = ConfigDict(populate_by_name=True)
    
    group_id: int = Field(..., alias='groupId')


class GroupDeleteRequest(BaseModel):
    """Запрос на удаление группы"""
    model_config = ConfigDict(populate_by_name=True)
    
    group_id: int = Field(..., alias='groupId')
