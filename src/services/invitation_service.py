"""
Сервис для работы с приглашениями
РАЗРАБОТЧИК: BAGA
"""
from sqlalchemy.orm import Session
from typing import Optional

from src.models.invitation import Invitation
from src.models.user import User
from src.constants.constants import InvitationStatus


class InvitationService:
    """Сервис для работы с приглашениями в группы"""
    
    @staticmethod
    def create_invitation(
        db: Session,
        group_id: int,
        inviter_id: int,
        invitee_email: str
    ) -> tuple[Optional[Invitation], Optional[str]]:
        """
        Создает приглашение в группу
        
        TODO (BAGA):
        1. Проверить, что пользователь с таким email существует
        2. Проверить, что нет активного приглашения
        3. Создать приглашение
        4. Вернуть (Invitation, None) или (None, error_message)
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def accept_invitation(
        db: Session,
        invitation_id: int,
        user_email: str
    ) -> tuple[bool, Optional[str]]:
        """
        Принимает приглашение
        
        TODO (BAGA):
        1. Получить приглашение
        2. Проверить, что оно для этого пользователя
        3. Проверить статус PENDING
        4. Обновить статус на ACCEPTED
        5. Добавить пользователя в группу (GroupMember)
        6. Вернуть (True, None) или (False, error_message)
        """
        # TODO: Implement
        pass
    
    @staticmethod
    def decline_invitation(
        db: Session,
        invitation_id: int,
        user_email: str
    ) -> tuple[bool, Optional[str]]:
        """
        Отклоняет приглашение
        
        TODO (BAGA):
        1. Получить приглашение
        2. Проверить, что оно для этого пользователя
        3. Проверить статус PENDING
        4. Обновить статус на DECLINED
        5. Вернуть (True, None) или (False, error_message)
        """
        # TODO: Implement
        pass


