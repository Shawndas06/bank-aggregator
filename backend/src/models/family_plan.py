"""
Модели для семейного финансового плана.

FamilyObligation — обязательный платёж группы (аренда, ЖКХ, кредит и т.д.)
FamilyContribution — взнос участника в общий план
"""
import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, ForeignKey,
    Boolean, Text, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from src.database import Base


class ObligationStatus(str, enum.Enum):
    PENDING = "pending"       # Ожидает оплаты
    PAID = "paid"             # Оплачено
    OVERDUE = "overdue"       # Просрочено
    CANCELLED = "cancelled"   # Отменено


class ContributionStatus(str, enum.Enum):
    PROPOSED = "proposed"     # Предложен, ждёт подтверждения другим участником
    CONFIRMED = "confirmed"   # Подтверждён обоими
    CANCELLED = "cancelled"   # Отменён


class FamilyObligation(Base):
    """
    Обязательный платёж в семейном плане.

    Пример: 'Аренда квартиры', 35 000₽, 25 числа каждого месяца,
    ответственный: Иван.
    """
    __tablename__ = "family_obligations"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False, index=True)

    # Что платим
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    amount_kopecks = Column(Integer, nullable=False)  # Сумма в копейках — точная арифметика

    # Когда платим
    due_date = Column(DateTime, nullable=False)        # Конкретная дата платежа
    is_recurring = Column(Boolean, default=False)      # Ежемесячное обязательство?
    recurring_day = Column(Integer, nullable=True)     # День месяца для рекуррентных

    # Кто платит
    responsible_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Статус
    status = Column(SQLEnum(ObligationStatus), default=ObligationStatus.PENDING, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    paid_confirmed_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Второй участник подтвердил

    # Метаданные
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    group = relationship("Group")
    responsible_user = relationship("User", foreign_keys=[responsible_user_id])
    creator = relationship("User", foreign_keys=[created_by])

    @property
    def amount_rub(self) -> float:
        return self.amount_kopecks / 100.0

    def __repr__(self):
        return f"<FamilyObligation(id={self.id}, name={self.name}, amount={self.amount_rub}₽)>"


class FamilyContribution(Base):
    """
    Взнос участника в семейный план.

    Участник обещает добавить N рублей к определённой дате.
    Взнос не списывает деньги — это договорённость, которую подтверждает второй участник.
    """
    __tablename__ = "family_contributions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False, index=True)

    # Кто вносит
    contributor_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Сколько и когда
    amount_kopecks = Column(Integer, nullable=False)  # В копейках
    expected_date = Column(DateTime, nullable=False)   # Когда поступят деньги

    # Описание (необязательно)
    note = Column(String(500), nullable=True)

    # Статус согласования
    status = Column(SQLEnum(ContributionStatus), default=ContributionStatus.PROPOSED, nullable=False)
    confirmed_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Второй участник
    confirmed_at = Column(DateTime, nullable=True)

    # Факт получения (вручную помечается)
    received = Column(Boolean, default=False)
    received_at = Column(DateTime, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    group = relationship("Group")
    contributor = relationship("User", foreign_keys=[contributor_user_id])
    confirmer = relationship("User", foreign_keys=[confirmed_by])
    creator = relationship("User", foreign_keys=[created_by])

    @property
    def amount_rub(self) -> float:
        return self.amount_kopecks / 100.0

    def __repr__(self):
        return f"<FamilyContribution(id={self.id}, amount={self.amount_rub}₽, status={self.status})>"


class PlanSharedResource(Base):
    """
    Явное разрешение: какой счёт участник включил в семейный план.

    Включение счёта в план ≠ раскрытие всех операций партнёру.
    Видны только: баланс счёта и сумма взноса.
    """
    __tablename__ = "plan_shared_resources"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Что именно включено в план
    resource_type = Column(String(50), nullable=False)  # "account" | "fixed_amount"

    # Для типа "account"
    bank_client_id = Column(Integer, nullable=True)   # ID подключённого банка
    bank_account_id = Column(String(255), nullable=True)  # ID счёта в банке

    # Для типа "fixed_amount" — фиксированный обещанный взнос
    fixed_amount_kopecks = Column(Integer, nullable=True)

    # Что партнёр видит по этому ресурсу
    # "balance_only" — только текущий баланс (без деталей транзакций)
    # "none" — ничего (только факт включения)
    visibility = Column(String(50), default="balance_only", nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    group = relationship("Group")
    user = relationship("User")
