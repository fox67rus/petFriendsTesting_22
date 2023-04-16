# Негативные тесты на запрос данных питомцев
import pytest

from api import pf
from config import generate_string, russian_chars, chinese_chars, special_chars


@pytest.mark.negative
@pytest.mark.get
def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев с некорректным api ключом возвращает код 403
    """
    auth_key = {
        'key': 'very-invalid-api-key'
    }
    status, result, _ = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


@pytest.mark.xfail(reason='Баг в продукте - не верный ответ сервера')
@pytest.mark.get
@pytest.mark.parametrize("filter",
                         [
                             generate_string(255),
                             generate_string(1001),
                             russian_chars(),
                             russian_chars().upper(),
                             chinese_chars(),
                             special_chars(),
                             '123',
                         ],
                         ids=
                         [
                             '255 symbols',
                             'more than 1000 symbols',
                             'russian',
                             'RUSSIAN',
                             'chinese',
                             'specials',
                             'digit',
                         ])
def test_get_list_of_pets(get_key, filter):
    """
    Проверка негативных значений параметра filter. Статус код ответа 400, а не 500.
    """
    status, result, _ = pf.get_list_of_pets(get_key, filter)
    assert status == 400
