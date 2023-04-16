from time import time

import pytest
from tests.test_pet_friends import pf, valid_password, valid_email


@pytest.fixture
def get_key():
    """ Фикстура получения ключа аутентификации"""
    # Проверяем наличие ключа в переменной класса
    if pf.auth_key:
        print('\nИспользуем полученный ранее ключ')
        key = pf.auth_key
        return key
    # Если ключ отсутствует, то запрашиваем ключ api
    print('Получаем ключ с сервера')
    status, key, response_headers = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in key
    return key


@pytest.fixture
def delete_test_pets(get_key):
    """ Фикстура для удаления созданных в процессе тестирования питомцев после выполнения тестов """
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')
    pet_count = len(my_pets['pets'])
    yield
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')
    while len(my_pets['pets']) > pet_count:
        pet_id = my_pets['pets'][0]['id']
        pf.delete_pet(get_key, pet_id)
        _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')


@pytest.fixture(autouse=True)
def calc_test_time(request):
    """ Фикстура расчёта времени выполнения тестов """
    start_time = time()
    yield
    end_time = time()
    test_time = end_time - start_time

    with open('test_time.txt', 'a', encoding="utf-8") as f:
        f.write(
            f'Тест {request.function.__name__} из {request.fspath}.\n'
            f'Время теста {test_time} с.\n'
            f'=====\n')
