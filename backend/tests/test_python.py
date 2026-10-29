import pytest
from src.utils.validators import validate_email, validate_password_strength


@pytest.mark.parametrize('value,valid', [('user@example.test', True), ('', False), ('user@', False)])
def test_email_validation(value, valid):
    assert validate_email(value) is valid


@pytest.mark.parametrize('value,valid', [('Strong123', True), ('short', False),
                                         ('alllower123', False), ('ALLUPPER123', False),
                                         ('NoNumbersHere', False)])
def test_password_boundaries(value, valid):
    assert validate_password_strength(value)[0] is valid


def test_application_imports_and_openapi_contract():
    from main import app
    schema = app.openapi()
    assert '/health' in schema['paths']
    assert '/api/auth/sign-in' in schema['paths']
