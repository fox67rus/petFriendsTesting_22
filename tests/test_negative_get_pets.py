# Негативные тесты на запрос данных питомцев
import pytest

from api import pf


@pytest.mark.negative
@pytest.mark.get
def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев с некорректным api ключом возвращает код 403
    """
    auth_key = {
        'key': 'very-invalid-api-key'
    }
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
