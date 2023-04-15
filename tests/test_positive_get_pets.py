# Позитивные тесты на запрос данных питомцев
import pytest

from api import pf


@pytest.mark.get
@pytest.mark.parametrize("filter", ['', 'my_pets'], ids=['all pets', 'only my pets'])
def test_get_all_pets_with_valid_key(get_key, filter):
    """
    Проверяем что запрос всех питомцев на сайте или питомцев пользователя возвращает не пустой список и статус код 200.
    Заголовки ответа содержат обязательные значения: Content-type: aplication/json или application/xml
    Используется фикстура параметризации с позитивными сценариями.
    """
    status, result = pf.get_list_of_pets(get_key, filter)

    assert status == 200
    assert len(result['pets']) > 0
