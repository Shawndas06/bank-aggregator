"""
Сервис для семейного финансового плана.

Ключевой алгоритм: расчёт планового остатка по дням.

Плановый остаток на день D =
    включённые_доступные_средства
    + сумма подтверждённых взносов с датой <= D
    - сумма обязательств со статусом PENDING с датой <= D

Важные инварианты (по плану продукта):
 - Не считать один ресурс дважды (баланс счёта + уже зачисленный взнос)
 - Переводы между включёнными счетами — не новый доход семьи
 - Оплаченное обязательство не вычитать повторно из фактического остатка
 - Кредитный лимит не считать собственными деньгами
 - Хранить суммы в копейках, выдавать в рублях
"""
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from src.models.group import Group, GroupMember
from src.models.family_plan import (
    FamilyObligation, FamilyContribution, PlanSharedResource,
    ObligationStatus, ContributionStatus,
)


class FamilyPlanService:

    # ─── Обязательства ────────────────────────────────────────────────────────

    @staticmethod
    def create_obligation(
        db: Session,
        group_id: int,
        creator_id: int,
        name: str,
        amount_rub: float,
        due_date: datetime,
        responsible_user_id: int,
        description: Optional[str] = None,
        is_recurring: bool = False,
        recurring_day: Optional[int] = None,
    ) -> Tuple[Optional[FamilyObligation], Optional[str]]:
        # Проверка: создатель — участник группы
        if not FamilyPlanService._is_member(db, group_id, creator_id):
            return None, "Вы не являетесь участником группы"
        # Проверка: ответственный — тоже участник
        if not FamilyPlanService._is_member(db, group_id, responsible_user_id):
            return None, "Ответственный должен быть участником группы"

        amount_kopecks = round(amount_rub * 100)

        obligation = FamilyObligation(
            group_id=group_id,
            name=name,
            description=description,
            amount_kopecks=amount_kopecks,
            due_date=due_date,
            responsible_user_id=responsible_user_id,
            is_recurring=is_recurring,
            recurring_day=recurring_day,
            status=ObligationStatus.PENDING,
            created_by=creator_id,
        )
        db.add(obligation)
        db.commit()
        db.refresh(obligation)
        return obligation, None

    @staticmethod
    def list_obligations(
        db: Session,
        group_id: int,
        requester_id: int,
        include_paid: bool = False,
    ) -> Tuple[List[FamilyObligation], Optional[str]]:
        if not FamilyPlanService._is_member(db, group_id, requester_id):
            return [], "Вы не являетесь участником группы"

        q = db.query(FamilyObligation).filter(FamilyObligation.group_id == group_id)
        if not include_paid:
            q = q.filter(FamilyObligation.status == ObligationStatus.PENDING)
        return q.order_by(FamilyObligation.due_date).all(), None

    @staticmethod
    def mark_paid(
        db: Session,
        obligation_id: int,
        requester_id: int,
    ) -> Tuple[bool, Optional[str]]:
        ob = db.query(FamilyObligation).filter(FamilyObligation.id == obligation_id).first()
        if not ob:
            return False, "Обязательство не найдено"
        if not FamilyPlanService._is_member(db, ob.group_id, requester_id):
            return False, "Нет доступа"
        if ob.status == ObligationStatus.PAID:
            return False, "Уже оплачено"

        ob.status = ObligationStatus.PAID
        ob.paid_at = datetime.utcnow()
        ob.paid_confirmed_by = requester_id
        db.commit()
        return True, None

    @staticmethod
    def delete_obligation(
        db: Session,
        obligation_id: int,
        requester_id: int,
    ) -> Tuple[bool, Optional[str]]:
        ob = db.query(FamilyObligation).filter(FamilyObligation.id == obligation_id).first()
        if not ob:
            return False, "Не найдено"
        if not FamilyPlanService._is_member(db, ob.group_id, requester_id):
            return False, "Нет доступа"

        db.delete(ob)
        db.commit()
        return True, None

    # ─── Взносы ───────────────────────────────────────────────────────────────

    @staticmethod
    def create_contribution(
        db: Session,
        group_id: int,
        contributor_id: int,
        amount_rub: float,
        expected_date: datetime,
        note: Optional[str] = None,
    ) -> Tuple[Optional[FamilyContribution], Optional[str]]:
        if not FamilyPlanService._is_member(db, group_id, contributor_id):
            return None, "Вы не являетесь участником группы"

        contribution = FamilyContribution(
            group_id=group_id,
            contributor_user_id=contributor_id,
            amount_kopecks=round(amount_rub * 100),
            expected_date=expected_date,
            note=note,
            status=ContributionStatus.PROPOSED,
            created_by=contributor_id,
        )
        db.add(contribution)
        db.commit()
        db.refresh(contribution)
        return contribution, None

    @staticmethod
    def confirm_contribution(
        db: Session,
        contribution_id: int,
        confirmer_id: int,
    ) -> Tuple[bool, Optional[str]]:
        """Второй участник подтверждает взнос."""
        c = db.query(FamilyContribution).filter(FamilyContribution.id == contribution_id).first()
        if not c:
            return False, "Взнос не найден"
        if not FamilyPlanService._is_member(db, c.group_id, confirmer_id):
            return False, "Нет доступа"
        if c.contributor_user_id == confirmer_id:
            return False, "Нельзя подтвердить собственный взнос"
        if c.status != ContributionStatus.PROPOSED:
            return False, "Взнос уже обработан"

        c.status = ContributionStatus.CONFIRMED
        c.confirmed_by = confirmer_id
        c.confirmed_at = datetime.utcnow()
        db.commit()
        return True, None

    @staticmethod
    def cancel_contribution(
        db: Session,
        contribution_id: int,
        requester_id: int,
    ) -> Tuple[bool, Optional[str]]:
        c = db.query(FamilyContribution).filter(FamilyContribution.id == contribution_id).first()
        if not c:
            return False, "Не найдено"
        if not FamilyPlanService._is_member(db, c.group_id, requester_id):
            return False, "Нет доступа"

        c.status = ContributionStatus.CANCELLED
        db.commit()
        return True, None

    @staticmethod
    def mark_received(
        db: Session,
        contribution_id: int,
        requester_id: int,
    ) -> Tuple[bool, Optional[str]]:
        c = db.query(FamilyContribution).filter(FamilyContribution.id == contribution_id).first()
        if not c:
            return False, "Не найдено"
        if not FamilyPlanService._is_member(db, c.group_id, requester_id):
            return False, "Нет доступа"
        if c.received:
            return False, "Уже отмечен как полученный"

        c.received = True
        c.received_at = datetime.utcnow()
        db.commit()
        return True, None

    @staticmethod
    def list_contributions(
        db: Session,
        group_id: int,
        requester_id: int,
    ) -> Tuple[List[FamilyContribution], Optional[str]]:
        if not FamilyPlanService._is_member(db, group_id, requester_id):
            return [], "Нет доступа"
        contribs = (
            db.query(FamilyContribution)
            .filter(
                FamilyContribution.group_id == group_id,
                FamilyContribution.status != ContributionStatus.CANCELLED,
            )
            .order_by(FamilyContribution.expected_date)
            .all()
        )
        return contribs, None

    # ─── Общие ресурсы ────────────────────────────────────────────────────────

    @staticmethod
    def set_shared_resource(
        db: Session,
        group_id: int,
        user_id: int,
        resource_type: str,
        bank_client_id: Optional[int],
        bank_account_id: Optional[str],
        fixed_amount_kopecks: Optional[int],
        visibility: str = "balance_only",
    ) -> Tuple[Optional[PlanSharedResource], Optional[str]]:
        if not FamilyPlanService._is_member(db, group_id, user_id):
            return None, "Нет доступа"

        # Деактивируем старые
        existing = (
            db.query(PlanSharedResource)
            .filter(
                PlanSharedResource.group_id == group_id,
                PlanSharedResource.user_id == user_id,
                PlanSharedResource.is_active == True,
            )
            .all()
        )
        for r in existing:
            r.is_active = False

        resource = PlanSharedResource(
            group_id=group_id,
            user_id=user_id,
            resource_type=resource_type,
            bank_client_id=bank_client_id,
            bank_account_id=bank_account_id,
            fixed_amount_kopecks=fixed_amount_kopecks,
            visibility=visibility,
            is_active=True,
        )
        db.add(resource)
        db.commit()
        db.refresh(resource)
        return resource, None

    @staticmethod
    def get_shared_resources(
        db: Session,
        group_id: int,
        requester_id: int,
    ) -> Tuple[List[PlanSharedResource], Optional[str]]:
        if not FamilyPlanService._is_member(db, group_id, requester_id):
            return [], "Нет доступа"

        resources = (
            db.query(PlanSharedResource)
            .filter(
                PlanSharedResource.group_id == group_id,
                PlanSharedResource.is_active == True,
            )
            .all()
        )
        return resources, None

    # ─── Прогноз денежного потока ─────────────────────────────────────────────

    @staticmethod
    def calculate_forecast(
        db: Session,
        group_id: int,
        requester_id: int,
        included_balance_rub: float,  # Текущий баланс включённых ресурсов (передаётся явно)
        reserve_rub: float = 5000.0,  # Резерв на бытовые расходы
        days_ahead: int = 30,
    ) -> dict:
        """
        Рассчитывает плановый денежный поток на days_ahead дней.

        included_balance_rub — текущий баланс включённых счетов.
        Передаётся явно (не запрашивается из банка), чтобы не создавать
        зависимость от банковского API в расчёте.

        Ограничения, показываемые пользователю:
         - Считается только включённый ресурс (личные деньги неизвестны)
         - Неожиданные расходы не учтены
         - Взносы со статусом PROPOSED не гарантированы
        """
        if not FamilyPlanService._is_member(db, group_id, requester_id):
            return {"error": "Нет доступа"}

        now = datetime.utcnow()
        end_date = now + timedelta(days=days_ahead)

        # Предстоящие обязательства (PENDING, до end_date)
        obligations = (
            db.query(FamilyObligation)
            .filter(
                FamilyObligation.group_id == group_id,
                FamilyObligation.status == ObligationStatus.PENDING,
                FamilyObligation.due_date <= end_date,
                FamilyObligation.due_date >= now,
            )
            .order_by(FamilyObligation.due_date)
            .all()
        )

        # Подтверждённые взносы (до end_date, ещё не получены)
        contributions = (
            db.query(FamilyContribution)
            .filter(
                FamilyContribution.group_id == group_id,
                FamilyContribution.status == ContributionStatus.CONFIRMED,
                FamilyContribution.received == False,
                FamilyContribution.expected_date <= end_date,
                FamilyContribution.expected_date >= now,
            )
            .order_by(FamilyContribution.expected_date)
            .all()
        )

        # Строим посуточный план
        days_plan = []
        running_balance = included_balance_rub
        first_risk_date = None
        min_balance = running_balance

        total_obligations = sum(o.amount_rub for o in obligations)
        total_contributions = sum(c.amount_rub for c in contributions)

        # Индексируем события по дате
        events_by_date: dict = {}
        for ob in obligations:
            day_key = ob.due_date.strftime("%Y-%m-%d")
            events_by_date.setdefault(day_key, []).append({
                "type": "obligation",
                "id": ob.id,
                "name": ob.name,
                "amount_rub": -ob.amount_rub,  # Отрицательное — расход
                "responsible_user_id": ob.responsible_user_id,
            })

        for c in contributions:
            day_key = c.expected_date.strftime("%Y-%m-%d")
            events_by_date.setdefault(day_key, []).append({
                "type": "contribution",
                "id": c.id,
                "amount_rub": c.amount_rub,   # Положительное — приход
                "contributor_user_id": c.contributor_user_id,
                "status": c.status,
            })

        for i in range(days_ahead):
            day = now + timedelta(days=i)
            day_key = day.strftime("%Y-%m-%d")
            day_events = events_by_date.get(day_key, [])

            # Применяем события этого дня
            for ev in day_events:
                running_balance += ev["amount_rub"]

            planned_balance = round(running_balance, 2)
            is_risk = planned_balance < reserve_rub

            if is_risk and first_risk_date is None:
                first_risk_date = day_key

            if planned_balance < min_balance:
                min_balance = planned_balance

            days_plan.append({
                "date": day_key,
                "planned_balance": planned_balance,
                "events": day_events,
                "is_risk": is_risk,
            })

        return {
            "included_balance_rub": round(included_balance_rub, 2),
            "total_obligations_rub": round(total_obligations, 2),
            "total_contributions_rub": round(total_contributions, 2),
            "reserve_rub": round(reserve_rub, 2),
            "first_risk_date": first_risk_date,
            "min_balance_rub": round(min_balance, 2),
            "days": days_plan,
            "data_as_of": now.isoformat(),
            "disclaimer": (
                "Прогноз учитывает только включённые в план ресурсы и подтверждённые взносы. "
                "Личные расходы и неожиданные платежи не учтены. "
                "Взносы со статусом 'предложен' не включены в расчёт до подтверждения."
            ),
        }

    # ─── Вспомогательные ──────────────────────────────────────────────────────

    @staticmethod
    def _is_member(db: Session, group_id: int, user_id: int) -> bool:
        return db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
        ).first() is not None
