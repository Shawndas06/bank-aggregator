import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect

from src.models.savings_goal import SavingsGoal
from src.services.savings_service import SavingsService

pytestmark = pytest.mark.integration


def test_postgres_roundtrip_and_goal_state(live_db):
    goal, error = SavingsService.create_goal(live_db, 1001, 'CI roundtrip', 100)
    assert error is None
    assert SavingsService.contribute_to_goal(live_db, goal.id, 1001, 25) == (True, None)
    live_db.expire_all()
    assert live_db.get(SavingsGoal, goal.id).current_amount == 25
    assert {'users', 'payments', 'savings_goals', 'groups'} <= set(inspect(live_db.bind).get_table_names())


def test_api_startup_health_and_redis(live_db):
    from main import app
    from src.redis_client import redis_client
    key = 'ci:integration:roundtrip'
    try:
        assert redis_client.set(key, 'ok', ex=30)
        assert redis_client.get(key) in ('ok', b'ok')
        with TestClient(app) as client:
            response = client.get('/health')
            assert response.status_code == 200
            assert response.json()['data']['redis'] == 'healthy'
            assert client.get('/openapi.json').status_code == 200
            assert client.get('/api/accounts').status_code in (401, 403)
    finally:
        redis_client.delete(key)
