# Негативные тесты изменения питомцев
import pytest

from api import pf
import os


@pytest.mark.skip(reason="Баг в продукте - https://petfriends.skillfactory.ru/my_pets")
@pytest.mark.negative
@pytest.mark.put
def test_unsuccessful_update_another_user_pet_info(get_key, name='Ниндзя', animal_type='НЛО', age=999):
    """Проверяем возможность обновления информации о питомце другого пользователя. Ожидается отказ доступа"""

    # Получаем ключ auth_key и список питомцев на сайте

    _, my_pets = pf.get_list_of_pets(get_key, "")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа не равно 200 и имя питомца не заменилось
        assert status != 200

    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('Список питомцев пуст')


@pytest.mark.skip(reason="Баг в продукте - https://petfriends.skillfactory.ru/my_pets")
@pytest.mark.negative
@pytest.mark.put
def test_unsuccessful_update_self_pet_info_with_empty_type(get_key, name='Кото пёс', animal_type=' ', age=3):
    """Обновление данных питомца: новая порода пустая строка. Ожидается ответ 400"""

    # Получаем список своих питомцев

    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400
        assert status == 400

    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('Список питомцев пуст')
