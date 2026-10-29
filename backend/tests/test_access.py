import pytest

from src.constants.constants import GroupRole
from src.models.group import Group, GroupMember
from src.models.savings_goal import GoalStatus, SavingsGoal
from src.services.group_service import GroupService
from src.services.savings_service import SavingsService

pytestmark = pytest.mark.access


def test_another_user_cannot_contribute_or_read_goals(db):
    goal, _ = SavingsService.create_goal(db, 1, 'Private', 100)
    assert SavingsService.get_user_goals(db, 2) == []
    assert SavingsService.contribute_to_goal(db, goal.id, 2, 50)[0] is False
    db.expire_all()
    assert db.get(SavingsGoal, goal.id).current_amount == 0


@pytest.mark.parametrize('status', [GoalStatus.PAUSED, GoalStatus.CANCELLED, GoalStatus.COMPLETED])
def test_inactive_goal_does_not_change(db, status):
    goal, _ = SavingsService.create_goal(db, 1, 'Inactive', 100)
    goal.status = status
    db.commit()
    assert SavingsService.contribute_to_goal(db, goal.id, 1, 50)[0] is False
    db.expire_all()
    assert db.get(SavingsGoal, goal.id).current_amount == 0


@pytest.mark.parametrize('requester,new_role,allowed', [
    (GroupRole.OWNER, GroupRole.ADMIN, True),
    (GroupRole.ADMIN, GroupRole.MEMBER, True),
    (GroupRole.ADMIN, GroupRole.ADMIN, False),
    (GroupRole.ADMIN, GroupRole.OWNER, False),
    (GroupRole.MEMBER, GroupRole.ADMIN, False),
    (None, GroupRole.MEMBER, False),
])
def test_role_assignment_matrix(db, requester, new_role, allowed):
    group = Group(id=1, name='Family', owner_id=1)
    db.add(group)
    db.flush()
    if requester:
        db.add(GroupMember(group_id=1, user_id=1, role=requester))
    db.add(GroupMember(group_id=1, user_id=2, role=GroupRole.MEMBER))
    db.commit()
    result, _ = GroupService.update_member_role(db, 1, 2, new_role, 1)
    assert result is allowed
    db.expire_all()
    assert GroupService.get_member_role(db, 1, 2) == (new_role if allowed else GroupRole.MEMBER)


def test_owner_role_cannot_be_overwritten(db):
    db.add(Group(id=1, name='Family', owner_id=1))
    db.flush()
    db.add(GroupMember(group_id=1, user_id=1, role=GroupRole.OWNER))
    db.commit()
    assert GroupService.update_member_role(db, 1, 1, GroupRole.MEMBER, 1)[0] is False
    db.expire_all()
    assert GroupService.get_member_role(db, 1, 1) == GroupRole.OWNER
