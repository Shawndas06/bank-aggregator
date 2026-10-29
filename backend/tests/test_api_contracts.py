from datetime import date

import pytest
from fastapi.testclient import TestClient

from main import app
from src.database import get_db
from src.dependencies import get_current_user, get_current_verified_user
from src.models.user import User
from src.services.auth_service import AuthService


@pytest.fixture
def client(db):
    user = db.get(User, 1)
    user.is_verified = True
    db.commit()
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_current_verified_user] = lambda: user
    # No context manager: unit API contracts override DB and don't start production services.
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        test_client.close()
        app.dependency_overrides.clear()


def test_profile_wire_retains_fields_used_by_ui(client):
    response = client.get('/api/auth/me')
    assert response.status_code == 200
    data = response.json()['data']
    assert data['isVerified'] is True
    assert data['accountType'] == 'free'
    assert data['email'] == 'user1@example.test'
    assert data['phone'] is None
    assert data['avatarUrl'] is None


def test_loyalty_create_list_read_delete_roundtrip(client, db):
    payload = {'card_type': 'magnit', 'card_number': '1234567890128',
               'card_name': 'Test', 'barcode_type': 'EAN13'}
    created = client.post('/api/loyalty-cards', json=payload)
    assert created.status_code == 201, created.text
    card_id = created.json()['data']['card']['id']
    db.expire_all()
    rows = client.get('/api/loyalty-cards').json()['data']
    assert isinstance(rows, list) and len(rows) == 1
    assert rows[0]['id'] == card_id
    assert rows[0]['card_type'] == 'magnit'
    assert rows[0]['barcode_type'] == 'EAN13'
    assert 'card_number' not in rows[0]
    assert client.get(f'/api/loyalty-cards/{card_id}').json()['data']['card_number'] == payload['card_number']
    deleted = client.delete(f'/api/loyalty-cards/{card_id}')
    assert deleted.status_code == 200, deleted.text
    db.expire_all()
    assert client.get('/api/loyalty-cards').json()['data'] == []


def test_updated_auth_dependencies_preserve_passwords_and_verification(db):
    user, error = AuthService.create_user(db, 'new@example.test', 'StrongPass123', 'New',
                                          '+79000000123', date(1990, 1, 1))
    assert error is None
    assert AuthService.authenticate_user(db, user.email, 'StrongPass123')[0] is None
    assert AuthService.verify_user(db, user.email) is not None
    assert AuthService.authenticate_user(db, user.email, 'WrongPass123')[0] is None
    actual, error = AuthService.authenticate_user(db, user.email, 'StrongPass123')
    assert error is None and actual.id == user.id
