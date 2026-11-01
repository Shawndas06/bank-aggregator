"""
Pydantic-схемы для семейного финансового плана.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ObligationStatusEnum(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class ContributionStatusEnum(str, Enum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


# ─── Обязательства ────────────────────────────────────────────────────────────

class ObligationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название обязательства")
    description: Optional[str] = Field(None, max_length=1000)
    amount_rub: float = Field(..., gt=0, description="Сумма в рублях (> 0)")
    due_date: datetime = Field(..., description="Дата платежа")
    responsible_user_id: int = Field(..., description="ID ответственного участника")
    is_recurring: bool = Field(False, description="Ежемесячное?")
    recurring_day: Optional[int] = Field(None, ge=1, le=31)

    @validator("amount_rub")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Сумма должна быть больше 0")
        return round(v, 2)


class ObligationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    amount_rub: Optional[float] = Field(None, gt=0)
    due_date: Optional[datetime] = None
    responsible_user_id: Optional[int] = None
    status: Optional[ObligationStatusEnum] = None


class ObligationResponse(BaseModel):
    id: int
    group_id: int
    name: str
    description: Optional[str]
    amount_rub: float
    due_date: str
    is_recurring: bool
    recurring_day: Optional[int]
    responsible_user_id: int
    responsible_user_name: str
    status: str
    paid_at: Optional[str]
    created_by: int
    created_at: str


# ─── Взносы ───────────────────────────────────────────────────────────────────

class ContributionCreate(BaseModel):
    amount_rub: float = Field(..., gt=0, description="Сумма взноса в рублях")
    expected_date: datetime = Field(..., description="Ожидаемая дата поступления")
    note: Optional[str] = Field(None, max_length=500)

    @validator("amount_rub")
    def amount_positive(cls, v):
        return round(v, 2)


class ContributionResponse(BaseModel):
    id: int
    group_id: int
    contributor_user_id: int
    contributor_name: str
    amount_rub: float
    expected_date: str
    note: Optional[str]
    status: str
    confirmed_by: Optional[int]
    confirmed_by_name: Optional[str]
    received: bool
    received_at: Optional[str]
    created_at: str


# ─── Общий ресурс ─────────────────────────────────────────────────────────────

class SharedResourceCreate(BaseModel):
    resource_type: str = Field(..., description="'account' или 'fixed_amount'")
    bank_client_id: Optional[int] = None
    bank_account_id: Optional[str] = None
    fixed_amount_kopecks: Optional[int] = Field(None, ge=0)
    visibility: str = Field("balance_only", description="'balance_only' или 'none'")


class SharedResourceResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    resource_type: str
    bank_client_id: Optional[int]
    bank_account_id: Optional[str]
    fixed_amount_rub: Optional[float]
    visibility: str
    is_active: bool


# ─── Расчёт баланса по дням ───────────────────────────────────────────────────

class DayBalanceItem(BaseModel):
    date: str               # "2026-11-05"
    planned_balance: float  # Плановый остаток на конец дня (в рублях)
    events: List[dict]      # Список событий этого дня (платежи/взносы)
    is_risk: bool           # True, если баланс падает ниже резерва


class ForecastResponse(BaseModel):
    """Прогноз денежного потока на ближайшие 30 дней."""
    included_balance_rub: float      # Текущий общий баланс включённых ресурсов
    total_obligations_rub: float     # Сумма всех предстоящих обязательств
    total_contributions_rub: float   # Сумма подтверждённых взносов
    reserve_rub: float               # Резерв на бытовые расходы
    first_risk_date: Optional[str]   # Первая дата, когда деньги могут закончиться
    min_balance_rub: float           # Минимальный плановый остаток за период
    days: List[DayBalanceItem]       # Посуточный план
    data_as_of: str                  # Время расчёта
    disclaimer: str                  # Предупреждение об ограничениях прогноза
