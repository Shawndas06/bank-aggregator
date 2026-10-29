import pytest

from src.config import settings
from src.models.account import BankAccount
from src.models.payment import Payment
from src.models.user import User
from src.services.account_service import AccountService
from src.services.payment_service import PaymentService

pytestmark = [pytest.mark.calculations, pytest.mark.access]


@pytest.mark.parametrize('debug', [False, True])
@pytest.mark.parametrize('balance', [None, {}, {'amount': None}, {'amount': 'NaN'},
                                     {'amount': float('inf')}, {'amount': 100, 'currency': 'USD'},
                                     {'amount': 9}, RuntimeError('bank unavailable')])
@pytest.mark.parametrize('kind', ['internal', 'card', 'utility', 'premium'])
def test_unverified_funds_never_create_payment(db, monkeypatch, debug, balance, kind):
    monkeypatch.setattr(settings, 'DEBUG', debug)
    account = BankAccount(user_id=1, bank_id=1, account_id='source', account_name='Source')
    db.add(account)
    recipient = db.get(User, 2)
    recipient.phone, recipient.is_verified = '+79000000002', True
    db.commit()
    def get_balance(*args, **kwargs):
        if isinstance(balance, Exception):
            raise balance
        return balance
    monkeypatch.setattr(AccountService, 'get_account_balance', get_balance)
    if kind == 'internal':
        result, error = PaymentService.create_internal_transfer(db, 1, account.id, recipient.phone, 10)
    elif kind == 'card':
        result, error = PaymentService.create_card_transfer(db, 1, account.id, '0000000000000000', 'Recipient', 10)
    elif kind == 'utility':
        result, error = PaymentService.create_utility_payment(db, 1, account.id, 'mobile', 'test', 'test', 10)
    else:
        result, error = PaymentService.create_premium_payment(db, 1, account.id, 10)
    assert result is None and error
    db.expire_all()
    assert db.query(Payment).count() == 0


@pytest.mark.parametrize('amount', [0, -1, float('nan'), float('inf'), float('-inf')])
def test_invalid_amount_rejected_before_bank_access(db, monkeypatch, amount):
    def unexpected(*args, **kwargs):
        pytest.fail('Invalid amount must be rejected before contacting bank')
    monkeypatch.setattr(AccountService, 'get_account_balance', unexpected)
    assert PaymentService._check_balance(db, 1, BankAccount(account_id='source', bank_id=1), amount)


@pytest.mark.parametrize('amount,balance,accepted', [(10, 10, True), (10.01, 10, False), (0.25, 0.25, True)])
def test_exact_balance_boundary(db, monkeypatch, amount, balance, accepted):
    monkeypatch.setattr(AccountService, 'get_account_balance', lambda *args: {'amount': balance, 'currency': 'RUB'})
    error = PaymentService._check_balance(db, 1, BankAccount(account_id='source', bank_id=1), amount)
    assert (error is None) is accepted
