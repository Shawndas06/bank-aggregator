"""
Скрипт создания демонстрационного сценария 'Семейный мультибанк'.
Соответствует точно сценарию из документа 'код.ing':
 - В план включено 55 000 ₽.
 - До следующего дохода предстоят платежи 35 000 ₽ и 25 000 ₽.
 - Нехватка 5 000 ₽.
 - Второй участник подтверждает взнос 8 000 ₽, минимальный остаток становится 3 000 ₽.
"""
from datetime import datetime, timedelta, date
from src.database import SessionLocal, create_tables
from src.models.user import User
from src.models.group import Group, GroupMember
from src.models.family_plan import (
    FamilyObligation, FamilyContribution, PlanSharedResource,
    ObligationStatus, ContributionStatus
)
from src.constants.constants import GroupRole, AccountType
from src.utils.security import hash_password


def seed_demo_scenario():
    print("🌱 Инициализация демонстрационных данных 'Семейный мультибанк'...")
    create_tables()
    db = SessionLocal()

    try:
        # 1. Создаем двух участников пары
        password_hash = hash_password("Password123!")

        user_alex = db.query(User).filter(User.email == "alex@demo.ru").first()
        if not user_alex:
            user_alex = User(
                email="alex@demo.ru",
                password_hash=password_hash,
                name="Алексей Иванов",
                phone="+79991112233",
                birth_date=date(1995, 5, 20),
                account_type=AccountType.FREE,
                is_verified=True
            )
            db.add(user_alex)
            db.commit()
            db.refresh(user_alex)
            print("  ✅ Создан пользователь Алексей (alex@demo.ru)")
        else:
            print("  ℹ️ Пользователь Алексей уже существует")

        user_anna = db.query(User).filter(User.email == "anna@demo.ru").first()
        if not user_anna:
            user_anna = User(
                email="anna@demo.ru",
                password_hash=password_hash,
                name="Анна Иванова",
                phone="+79994445566",
                birth_date=date(1996, 8, 15),
                account_type=AccountType.FREE,
                is_verified=True
            )
            db.add(user_anna)
            db.commit()
            db.refresh(user_anna)
            print("  ✅ Создана пользователь Анна (anna@demo.ru)")
        else:
            print("  ℹ️ Пользователь Анна уже существует")

        # 2. Создаем семейную группу
        group = db.query(Group).filter(Group.name == "Семейный бюджет").first()
        if not group:
            group = Group(
                name="Семейный бюджет",
                owner_id=user_alex.id
            )
            db.add(group)
            db.commit()
            db.refresh(group)

            # Добавляем участников
            m1 = GroupMember(group_id=group.id, user_id=user_alex.id, role=GroupRole.OWNER)
            m2 = GroupMember(group_id=group.id, user_id=user_anna.id, role=GroupRole.MEMBER)
            db.add_all([m1, m2])
            db.commit()
            print(f"  ✅ Создана группа 'Семейный бюджет' (ID: {group.id}) с Алексеем и Анной")
        else:
            print(f"  ℹ️ Группа 'Семейный бюджет' уже существует (ID: {group.id})")

        # Очистим старые обязательства/взносы для группы, чтобы тест был чистым
        db.query(FamilyObligation).filter(FamilyObligation.group_id == group.id).delete()
        db.query(FamilyContribution).filter(FamilyContribution.group_id == group.id).delete()
        db.query(PlanSharedResource).filter(PlanSharedResource.group_id == group.id).delete()
        db.commit()

        # 3. Включенные ресурсы (выборочное раскрытие)
        # Алексей включает ресурс на 30 000 ₽ (balance_only)
        r1 = PlanSharedResource(
            group_id=group.id,
            user_id=user_alex.id,
            resource_type="fixed_amount",
            fixed_amount_kopecks=3000000,  # 30 000 ₽
            visibility="balance_only",
            is_active=True
        )
        # Анна включает ресурс на 25 000 ₽ (balance_only)
        r2 = PlanSharedResource(
            group_id=group.id,
            user_id=user_anna.id,
            resource_type="fixed_amount",
            fixed_amount_kopecks=2500000,  # 25 000 ₽
            visibility="balance_only",
            is_active=True
        )
        db.add_all([r1, r2])
        db.commit()
        print("  ✅ Настроены включённые семейные ресурсы: 30 000 ₽ + 25 000 ₽ = 55 000 ₽")

        # 4. Предстоящие обязательства
        now = datetime.utcnow()
        # Обязательство 1: Аренда 35 000 ₽ через 4 дня (платит Алексей)
        ob1 = FamilyObligation(
            group_id=group.id,
            name="Аренда квартиры",
            description="Оплата собственнику по договору",
            amount_kopecks=3500000,  # 35 000 ₽
            due_date=now + timedelta(days=4),
            responsible_user_id=user_alex.id,
            is_recurring=True,
            recurring_day=(now + timedelta(days=4)).day,
            status=ObligationStatus.PENDING,
            created_by=user_alex.id
        )

        # Обязательство 2: Платеж по автокредиту 25 000 ₽ через 9 дней (платит Анна)
        ob2 = FamilyObligation(
            group_id=group.id,
            name="Автокредит и страховка",
            description="Ежемесячный взнос",
            amount_kopecks=2500000,  # 25 000 ₽
            due_date=now + timedelta(days=9),
            responsible_user_id=user_anna.id,
            is_recurring=True,
            recurring_day=(now + timedelta(days=9)).day,
            status=ObligationStatus.PENDING,
            created_by=user_anna.id
        )
        db.add_all([ob1, ob2])
        db.commit()
        print("  ✅ Добавлены обязательства: Аренда (35 000 ₽) и Автокредит (25 000 ₽)")
        print("     -> Итого обязательств: 60 000 ₽ при балансе 55 000 ₽ (кассовый разрыв 5 000 ₽)")

        # 5. Согласованный взнос от Анны: 8 000 ₽ со статусом PROPOSED к 7-му дню
        # В интерфейсе Алексей может подтвердить этот взнос в 1 клик!
        contr = FamilyContribution(
            group_id=group.id,
            contributor_user_id=user_anna.id,
            amount_kopecks=800000,  # 8 000 ₽
            expected_date=now + timedelta(days=7),
            note="Аванс за проект, переведу до платежа по кредиту",
            status=ContributionStatus.PROPOSED,
            created_by=user_anna.id
        )
        db.add(contr)
        db.commit()
        print("  ✅ Добавлен предложенный взнос: 8 000 ₽ от Анны (ожидает подтверждения Алексея)")
        print("\n🎉 Демо-сценарий готов к показу на защите!")
        print("--------------------------------------------------")
        print("Логин 1 (Алексей): alex@demo.ru / Password123!")
        print("Логин 2 (Анна):    anna@demo.ru / Password123!")
        print(f"Группа:           ID {group.id} ('Семейный бюджет')")
        print("--------------------------------------------------")

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка заполнения демо-данных: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_scenario()
