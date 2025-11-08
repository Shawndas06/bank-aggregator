"""
Сервис для работы с приглашениями
"""
import logging
from sqlalchemy.orm import Session
from typing import Optional, Tuple

from src.models.invitation import Invitation
from src.models.user import User
from src.models.group import GroupMember
from src.constants.constants import InvitationStatus

logger = logging.getLogger(__name__)


class InvitationService:
    """Сервис для работы с приглашениями в группы"""
    
    @staticmethod
    def create_invitation(
        db: Session,
        group_id: int,
        inviter_id: int,
        invitee_email: str
    ) -> Tuple[Optional[Invitation], Optional[str]]:
        """
        Создаёт приглашение в группу
        
        Returns:
            (Invitation, None) если успешно
            (None, error_message) если ошибка
        """
        # Проверяем что пользователь существует
        invitee = db.query(User).filter(User.email == invitee_email).first()
        if not invitee:
            return None, "Пользователь с таким email не найден"
        
        # Проверяем что уже не член группы
        existing_member = (
            db.query(GroupMember)
            .filter(GroupMember.group_id == group_id, GroupMember.user_id == invitee.id)
            .first()
        )
        if existing_member:
            return None, "Пользователь уже является членом группы"
        
        # Проверяем нет ли активного приглашения
        existing_invitation = (
            db.query(Invitation)
            .filter(
                Invitation.group_id == group_id,
                Invitation.invitee_email == invitee_email,
                Invitation.status == InvitationStatus.PENDING
            )
            .first()
        )
        if existing_invitation:
            return None, "Приглашение уже отправлено"
        
        # Создаём приглашение
        invitation = Invitation(
            group_id=group_id,
            inviter_id=inviter_id,
            invitee_email=invitee_email,
            status=InvitationStatus.PENDING
        )
        
        db.add(invitation)
        db.commit()
        db.refresh(invitation)
        
        logger.info(f"Создано приглашение {invitation.id} в группу {group_id}")
        return invitation, None
    
    @staticmethod
    def accept_invitation(
        db: Session,
        invitation_id: int,
        user_email: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Принимает приглашение
        
        Returns:
            (True, None) если успешно
            (False, error_message) если ошибка
        """
        invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
        
        if not invitation:
            return False, "Приглашение не найдено"
        
        if invitation.invitee_email != user_email:
            return False, "Это приглашение не для вас"
        
        if invitation.status != InvitationStatus.PENDING:
            return False, "Приглашение уже обработано"
        
        # Находим пользователя
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            return False, "Пользователь не найден"
        
        # Обновляем статус приглашения
        invitation.status = InvitationStatus.ACCEPTED
        
        # Добавляем в группу
        member = GroupMember(group_id=invitation.group_id, user_id=user.id)
        db.add(member)
        
        db.commit()
        
        logger.info(f"Приглашение {invitation_id} принято пользователем {user.id}")
        return True, None
    
    @staticmethod
    def decline_invitation(
        db: Session,
        invitation_id: int,
        user_email: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Отклоняет приглашение
        
        Returns:
            (True, None) если успешно
            (False, error_message) если ошибка
        """
        invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
        
        if not invitation:
            return False, "Приглашение не найдено"
        
        if invitation.invitee_email != user_email:
            return False, "Это приглашение не для вас"
        
        if invitation.status != InvitationStatus.PENDING:
            return False, "Приглашение уже обработано"
        
        # Обновляем статус
        invitation.status = InvitationStatus.DECLINED
        db.commit()
        
        logger.info(f"Приглашение {invitation_id} отклонено")
        return True, None
