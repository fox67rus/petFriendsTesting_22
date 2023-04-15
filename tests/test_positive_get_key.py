# Позитивные тесты на запрос ключа аутентификации
import pytest

from api import pf
from config import valid_email, valid_password


@pytest.mark.get
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """
    Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key
    """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result, response_headers = pf.get_api_key(email, password)

    # Сверяем статус и результат
    assert status == 200
    assert 'key' in result
    assert response_headers['Content-Type'] == 'application/json' or 'application/xml'
