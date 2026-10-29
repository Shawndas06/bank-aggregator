from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

import src.services.analytics_service as analytics
from src.models.payment import Payment, PaymentStatus, PaymentType

pytestmark = pytest.mark.calculations


class FixedClock(datetime):
    @classmethod
    def now(cls, tz=None):
        value = cls(2030, 1, 20, 12)
        return value if tz is None else value.replace(tzinfo=timezone.utc).astimezone(tz)

    @classmethod
    def utcnow(cls):
        return cls(2030, 1, 20, 12)


@pytest.mark.parametrize('format', ['naive', 'utc', 'offset'])
@pytest.mark.parametrize('reverse', [False, True])
def test_overview_and_categories_reconcile_across_zones_months_and_order(db, monkeypatch, format, reverse):
    monkeypatch.setattr(analytics, 'datetime', FixedClock)
    def stamp(value):
        parsed = datetime.fromisoformat(value)
        if format == 'naive':
            return parsed.isoformat()
        parsed = parsed.replace(tzinfo=timezone.utc)
        if format == 'offset':
            return parsed.astimezone(timezone(timedelta(hours=3))).isoformat()
        return parsed.isoformat().replace('+00:00', 'Z')
    rows = [
        ('2029-12-31T23:59:59', -20, 'debit'),
        ('2030-01-01T00:00:00', -0.1, 'debit'),
        ('2030-01-15T12:00:00', -0.2, 'debit'),
        ('2030-01-16T12:00:00', 100.25, 'credit'),
        ('2030-02-01T00:00:00', -999, 'debit'),
    ]
    transactions = [dict(id=str(i), date=stamp(day), amount=amount, type=kind,
                         mccCode='5411', description='Groceries') for i, (day, amount, kind) in enumerate(rows)]
    if reverse:
        transactions.reverse()
    for source, recipient, amount, status in [
        (1, None, 10.05, PaymentStatus.COMPLETED),
        (2, 1, 5.25, PaymentStatus.COMPLETED),
        (1, None, 50, PaymentStatus.PENDING),
        (1, None, 60, PaymentStatus.FAILED),
        (1, None, 70, PaymentStatus.CANCELLED),
    ]:
        db.add(Payment(user_id=source, to_user_id=recipient, amount=amount,
                       status=status, payment_type=PaymentType.UTILITIES,
                       completed_at=datetime(2030, 1, 15)))
    db.commit()
    service = analytics.AnalyticsService(db, None)
    service.account_service = SimpleNamespace(
        get_user_accounts=lambda *args: [{'accountId': 'a', 'clientId': 1}],
        get_account_balance=lambda *args: {'amount': 100, 'currency': 'RUB'},
        get_account_transactions=lambda *args: transactions,
    )
    overview = service.get_user_overview(1)
    assert overview['currentMonth']['expenses'] == 10.35
    assert overview['currentMonth']['income'] == 105.5
    assert overview['totalBalance'] == 100
    categories = service.get_categories_breakdown(1, stamp('2030-01-01T00:00:00'), stamp('2030-01-31T23:59:59'))
    amounts = {category['category']: category['amount'] for category in categories}
    assert sorted(amounts.values()) == [0.3, 10.05]
    assert sorted(category['amount'] for category in overview['topCategories']) == [0.3, 10.05]
    assert sum(category['count'] for category in categories) == 3


def test_decimal_category_sum_has_no_binary_float_residue(db):
    service = analytics.AnalyticsService(db, None)
    service.account_service = SimpleNamespace(
        get_user_accounts=lambda *args: [{'accountId': 'a', 'clientId': 1}],
        get_account_transactions=lambda *args: [
            dict(id=str(i), date='2030-01-01T12:00:00', amount=amount, type='debit',
                 mccCode='5411', description='Groceries') for i, amount in enumerate([0.1, 0.2])],
    )
    assert service.get_categories_breakdown(1)[0]['amount'] == 0.3
