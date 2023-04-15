import functools
from datetime import datetime

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


@pytest.fixture
def log(request):
    start_time = datetime.now()
    yield
    end_time = datetime.now()

    print()  # название теста

    with open('log.txt', 'a', encoding="utf-8") as f:
        f.write(
            f'Тест {request.function.__name__}. Начало в {start_time}, окончание в {end_time} , тест шёл {end_time - start_time} \n')


def log_api(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        signature = func(*args, **kwargs)
        status = str(signature[0])
        result = str(signature[1])
        request = str(signature[2:4])
        responce_headers = str(signature[4:])
        with open('log.txt', 'w', encoding='utf8') as f:
            f.write(f'''Информация запроса:
------------------
Статус запроса:
{status}
Параметры запроса:
{request}
Информация ответа:
------------------
Тело ответа:
{result}
Заголовок ответа:
{responce_headers}''')

    return wrapper
