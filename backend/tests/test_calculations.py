from datetime import datetime
from types import SimpleNamespace

import pytest

from src.models.savings_goal import FamilyBudgetLimit, GoalStatus, SavingsGoal
from src.services.savings_service import FamilyBudgetService, SavingsService

pytestmark = pytest.mark.calculations


@pytest.mark.parametrize('current,target,percentage,remaining', [
    (0, 100, 0, 100), (25, 100, 25, 75), (100, 100, 100, 0),
    (150, 100, 150, -50), (0, 0, 0, 0), (0.25, 1, 25, 0.75),
])
def test_goal_progress(current, target, percentage, remaining):
    deadline = datetime(2030, 1, 1)
    goal = SimpleNamespace(current_amount=current, target_amount=target, target_date=deadline)
    result = SavingsService.calculate_progress(goal)
    assert result['progress_percentage'] == percentage
    assert result['remaining_amount'] == remaining
    assert result['estimated_completion_date'] == deadline


@pytest.mark.parametrize('daily,monthly,day_spent,month_spent,amount,exceeded', [
    (100, 1000, 90, 900, 10, False),
    (100, 1000, 90, 900, 10.01, True),
    (1000, 100, 0, 90, 10, False),
    (1000, 100, 0, 90, 10.01, True),
    (0, 0, 100, 100, 999999, False),
    (0, 100, 1000, 90, 11, True),
    (100, 0, 90, 1000, 11, True),
    (100, 100, 0, 0, 0, False),
])
def test_spending_boundaries(db, daily, monthly, day_spent, month_spent, amount, exceeded):
    db.add(FamilyBudgetLimit(group_id=1, user_id=1, daily_limit=daily,
                            monthly_limit=monthly, current_day_spent=day_spent,
                            current_month_spent=month_spent))
    db.commit()
    actual, reason = FamilyBudgetService.check_limit_exceeded(db, 1, 1, amount)
    assert actual is exceeded
    assert bool(reason) is exceeded


def test_contributions_persist_and_complete_only_at_target(db):
    goal, error = SavingsService.create_goal(db, 1, 'Test', 100)
    assert error is None
    for amount, expected, status in [(25, 25, GoalStatus.ACTIVE), (50, 75, GoalStatus.ACTIVE),
                                     (25, 100, GoalStatus.COMPLETED)]:
        assert SavingsService.contribute_to_goal(db, goal.id, 1, amount) == (True, None)
        db.expire_all()
        saved = db.get(SavingsGoal, goal.id)
        assert saved.current_amount == expected
        assert saved.status == status
    assert saved.completed_at is not None
    assert SavingsService.contribute_to_goal(db, goal.id, 1, 10)[0] is False
    db.expire_all()
    assert db.get(SavingsGoal, goal.id).current_amount == 100


def test_limit_is_scoped_to_member_and_group(db):
    db.add(FamilyBudgetLimit(group_id=1, user_id=1, daily_limit=1,
                            current_day_spent=1, current_month_spent=1))
    db.commit()
    assert FamilyBudgetService.check_limit_exceeded(db, 1, 1, 1)[0] is True
    assert FamilyBudgetService.check_limit_exceeded(db, 2, 1, 1) == (False, None)
    assert FamilyBudgetService.check_limit_exceeded(db, 1, 2, 1) == (False, None)
