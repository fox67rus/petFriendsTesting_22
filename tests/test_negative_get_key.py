# Негативные тесты на запрос ключа аутентификации
import pytest

from api import pf
from config import valid_email, valid_password


@pytest.mark.negative
@pytest.mark.get
def test_get_api_key_for_invalid_user(email='free-user@mymail.com', password='pass'):
    """
    Проверяем что запрос api ключа для незарегистрированного пользователя возвращает статус 403
    """
    status, _ = pf.get_api_key(email, password)
    assert status == 403
