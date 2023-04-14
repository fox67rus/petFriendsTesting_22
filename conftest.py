import functools
from datetime import datetime

import pytest
from tests.test_pet_friends import pf, valid_password, valid_email


@pytest.fixture()
def get_key():
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    status, key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in key
    return key


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
