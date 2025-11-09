"""
Сервис для работы с платежами
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from datetime import datetime
from src.models.payment import Payment, PaymentType, PaymentStatus
from src.models.user import User
from src.models.account import BankAccount


class PaymentService:
    """Сервис для управления платежами"""
    
    @staticmethod
    def search_user_by_phone(db: Session, phone: str) -> Optional[User]:
        """Поиск пользователя по номеру телефона"""
        return db.query(User).filter(User.phone == phone, User.is_verified == True).first()
    
    @staticmethod
    def create_internal_transfer(
        db: Session,
        user_id: int,
        from_account_id: int,
        to_phone: str,
        amount: float,
        description: Optional[str] = None
    ) -> Tuple[Optional[Payment], Optional[str]]:
        """
        Перевод зарегистрированному пользователю по телефону
        (внутри нашей системы, без использования Bank API)
        """
        # Проверяем счет отправителя
        from_account = db.query(BankAccount).filter(
            BankAccount.id == from_account_id,
            BankAccount.user_id == user_id
        ).first()
        
        if not from_account:
            return None, "Счет отправителя не найден"
        
        # Ищем получателя по телефону
        recipient = PaymentService.search_user_by_phone(db, to_phone)
        
        if not recipient:
            return None, f"Пользователь с номером {to_phone} не найден в системе"
        
        if recipient.id == user_id:
            return None, "Нельзя переводить самому себе"
        
        # Создаем платеж
        payment = Payment(
            user_id=user_id,
            payment_type=PaymentType.TO_PERSON,
            amount=amount,
            currency="RUB",
            from_account_id=from_account_id,
            from_account_name=from_account.account_name,
            to_user_id=recipient.id,
            to_phone=to_phone,
            to_name=recipient.name,
            description=description,
            status=PaymentStatus.COMPLETED,  # Внутренний перевод сразу completed
            completed_at=datetime.utcnow()
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        return payment, None
    
    @staticmethod
    def create_card_transfer(
        db: Session,
        user_id: int,
        from_account_id: int,
        to_account: str,
        to_name: str,
        amount: float,
        description: Optional[str] = None
    ) -> Tuple[Optional[Payment], Optional[str]]:
        """Перевод на карту (номер счета)"""
        from_account = db.query(BankAccount).filter(
            BankAccount.id == from_account_id,
            BankAccount.user_id == user_id
        ).first()
        
        if not from_account:
            return None, "Счет отправителя не найден"
        
        payment = Payment(
            user_id=user_id,
            payment_type=PaymentType.CARD_TO_CARD,
            amount=amount,
            currency="RUB",
            from_account_id=from_account_id,
            from_account_name=from_account.account_name,
            to_account=to_account,
            to_name=to_name,
            description=description,
            status=PaymentStatus.PENDING  # Требует обработки через Bank API
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # TODO: Интеграция с Bank API POST /payments
        # payment.bank_payment_id = ...
        # payment.status = PaymentStatus.COMPLETED
        # payment.completed_at = datetime.utcnow()
        
        return payment, None
    
    @staticmethod
    def create_utility_payment(
        db: Session,
        user_id: int,
        from_account_id: int,
        payment_type: str,
        provider: str,
        account_number: str,
        amount: float
    ) -> Tuple[Optional[Payment], Optional[str]]:
        """Оплата услуг (ЖКХ, связь, интернет и т.д.)"""
        from_account = db.query(BankAccount).filter(
            BankAccount.id == from_account_id,
            BankAccount.user_id == user_id
        ).first()
        
        if not from_account:
            return None, "Счет отправителя не найден"
        
        # Маппинг типов
        type_map = {
            "mobile": PaymentType.MOBILE,
            "utilities": PaymentType.UTILITIES,
            "internet": PaymentType.INTERNET,
            "tv": PaymentType.TV,
            "phone": PaymentType.PHONE,
            "electricity": PaymentType.ELECTRICITY,
        }
        
        ptype = type_map.get(payment_type, PaymentType.UTILITIES)
        
        payment = Payment(
            user_id=user_id,
            payment_type=ptype,
            amount=amount,
            currency="RUB",
            from_account_id=from_account_id,
            from_account_name=from_account.account_name,
            to_name=provider,
            to_account=account_number,
            description=f"Оплата {provider} - {account_number}",
            status=PaymentStatus.COMPLETED,  # Упрощенно - сразу completed
            completed_at=datetime.utcnow()
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        return payment, None
    
    @staticmethod
    def get_user_payments(
        db: Session,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[Payment]:
        """Получить историю платежей пользователя"""
        return db.query(Payment).filter(
            Payment.user_id == user_id
        ).order_by(Payment.created_at.desc()).offset(offset).limit(limit).all()
    
    @staticmethod
    def create_premium_payment(
        db: Session,
        user_id: int,
        from_account_id: int,
        amount: float = 299.0
    ) -> Tuple[Optional[Payment], Optional[str]]:
        """Создать платеж за Premium подписку"""
        from_account = db.query(BankAccount).filter(
            BankAccount.id == from_account_id,
            BankAccount.user_id == user_id
        ).first()
        
        if not from_account:
            return None, "Счет для оплаты не найден"
        
        payment = Payment(
            user_id=user_id,
            payment_type=PaymentType.PREMIUM,
            amount=amount,
            currency="RUB",
            from_account_id=from_account_id,
            from_account_name=from_account.account_name,
            to_name="Bank Aggregator Premium",
            description="Оплата подписки Premium на 1 месяц",
            status=PaymentStatus.COMPLETED,
            completed_at=datetime.utcnow()
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        return payment, None

