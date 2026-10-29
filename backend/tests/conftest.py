import os
from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

# Register every model, including those not exported from src.models.
import src.models  # noqa: F401
import src.models.loyalty_card  # noqa: F401
import src.models.payment  # noqa: F401
import src.models.savings_goal  # noqa: F401
from src.database import Base
from src.models.user import User


@pytest.fixture
def db():
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([
            User(id=i, email=f'user{i}@example.test', name=f'User {i}',
                 birth_date=date(1990, 1, 1), password_hash='test-only')
            for i in (1, 2, 3)
        ])
        session.commit()
        yield session
    engine.dispose()


@pytest.fixture
def live_db():
    if os.environ.get('CI_INTEGRATION') != '1':
        pytest.fail('Integration tests require CI_INTEGRATION=1 and a disposable PostgreSQL/Redis environment')
    from src.database import engine
    assert engine.dialect.name == 'postgresql'
    Base.metadata.create_all(engine)
    with engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection, join_transaction_mode='create_savepoint') as session:
            session.add(User(id=1001, email='integration@example.test', name='CI',
                             birth_date=date(1990, 1, 1), password_hash='test-only'))
            session.commit()
            yield session
        transaction.rollback()
