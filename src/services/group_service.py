"""
Сервис для работы с группами
РАЗРАБОТЧИК: EZIRA
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from src.models.group import Group, GroupMember
from src.models.user import User
from src.constants.constants import AccountType, ACCOUNT_LIMITS


class GroupService:
    """Сервис для работы с группами"""
    
    @staticmethod
    def create_group(
        db: Session,
        name: str,
        owner_id: int,
        account_type: AccountType
    ) -> tuple[Optional[Group], Optional[str]]:
        """
        Создает новую группу
        
        TODO (EZIRA):
        1. Проверить лимит групп для типа аккаунта
        2. Создать группу
        3. Добавить владельца в члены группы
        4. Вернуть (Group, None) или (None, error_message)
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def get_user_groups(db: Session, user_id: int) -> List[Group]:
        """
        Получает список групп пользователя
        
        TODO (EZIRA):
        1. Получить все группы, где пользователь является членом
        2. Вернуть список групп
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def delete_group(
        db: Session,
        group_id: int,
        user_id: int
    ) -> tuple[bool, Optional[str]]:
        """
        Удаляет группу
        
        TODO (EZIRA):
        1. Получить группу
        2. Проверить, что пользователь - владелец
        3. Удалить всех членов
        4. Удалить группу
        5. Вернуть (True, None) или (False, error_message)
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def exit_group(
        db: Session,
        group_id: int,
        user_id: int
    ) -> tuple[bool, Optional[str]]:
        """
        Выход из группы
        
        TODO (EZIRA):
        1. Получить группу
        2. Проверить, что пользователь НЕ владелец
        3. Удалить членство
        4. Вернуть (True, None) или (False, error_message)
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def get_group_members(db: Session, group_id: int) -> List[User]:
        """
        Получает список членов группы
        
        TODO (EZIRA):
        1. Получить всех членов группы
        2. Вернуть список пользователей
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def can_add_member(
        db: Session,
        group_id: int,
        account_type: AccountType
    ) -> tuple[bool, Optional[str]]:
        """
        Проверяет, можно ли добавить нового члена
        
        TODO (EZIRA):
        1. Получить текущее количество членов
        2. Проверить лимит для типа аккаунта
        3. Вернуть (True, None) или (False, error_message)
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def is_user_member(db: Session, group_id: int, user_id: int) -> bool:
        """
        Проверяет, является ли пользователь членом группы
        
        TODO (EZIRA):
        1. Проверить наличие записи GroupMember
        2. Вернуть True/False
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def is_user_owner(db: Session, group_id: int, user_id: int) -> bool:
        """
        Проверяет, является ли пользователь владельцем группы
        
        TODO (EZIRA):
        1. Получить группу
        2. Проверить owner_id
        3. Вернуть True/False
        """
        # TODO: Implement
        pass


