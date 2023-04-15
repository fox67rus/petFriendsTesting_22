# Позитивные тесты на запрос данных питомцев
import pytest

from api import pf


@pytest.mark.get
def test_get_all_pets_with_valid_key(get_key, filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо ''
    """
    status, result = pf.get_list_of_pets(get_key, filter)

    assert status == 200
    assert len(result['pets']) > 0
