# Негативные тесты на запрос ключа аутентификации
import pytest

from api import pf
from config import valid_email, invalid_email, invalid_password


@pytest.mark.get
@pytest.mark.parametrize("email", ['', valid_email, invalid_email], ids=['empty', 'valid email', 'invalid email'])
@pytest.mark.parametrize("password", ['', invalid_password], ids=['empty', 'invalid password'])
def test_get_api_key_for_invalid_user(email, password):
    """
    Проверяем что запрос api ключа для незарегистрированного пользователя возвращает статус 403
    """
    status, result, _ = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    # return status, result, email, password
