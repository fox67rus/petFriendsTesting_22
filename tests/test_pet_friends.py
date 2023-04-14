import pytest

from module22.petFriendsTesting_22.api import PetFriends
from module22.petFriendsTesting_22.config import valid_email, valid_password
import os

pf = PetFriends()


@pytest.mark.get
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """
    Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key
    """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем статус и результат
    assert status == 200
    assert 'key' in result


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


@pytest.mark.post
def test_add_new_pet_with_valid_data(log, get_key, name='Рыжик', animal_type='кот',
                                     age='2', pet_photo='images/red.jpg'):
    """
    Проверяем что можно добавить питомца с корректными данными
    """
    # Получаем полный путь к файлу с изображением питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    # Сверяем статус и результат
    assert status == 200
    assert result['name'] == name


@pytest.mark.put
def test_successful_update_self_pet_info(get_key, name='Тыковка', animal_type='кошка', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    # _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('Список питомцев пуст')


@pytest.mark.delete
def test_successful_delete_self_pet(get_key):
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    # _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(get_key, 'Кексик', 'кот', '2', 'images/red.jpg')
        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(get_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# 10 дополнительных тестов
@pytest.mark.post
def test_add_new_pet_without_photo_valid_data(get_key, name='Снежок', animal_type='хаски', age='0'):
    """
    Проверяем простой метод добавления питомца с корректными данными
    """

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем статус и результат
    assert status == 200
    assert result['name'] == name


@pytest.mark.put
def test_successful_add_pets_correct_photo(get_key, pet_photo='images/dog.jpg'):
    """
    Проверяем, что можно добавить фото питомцу с корректным файлом изображения
    """
    # Получаем полный путь к файлу с изображением питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    # _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pets_photo(get_key, pet_photo, my_pets['pets'][0]['id'])

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('Список питомцев пуст')


# Негативные тесты
@pytest.mark.get
def test_get_api_key_for_invalid_user(email='free-user@mymail.com', password='pass'):
    """
    Проверяем что запрос api ключа для незарегистрированного пользователя возвращает статус 403
    """
    status, _ = pf.get_api_key(email, password)
    assert status == 403


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


@pytest.mark.post
@pytest.mark.negative
def test_add_new_pet_without_photo_negative_age(get_key, name='Гав', animal_type='котёнок', age='-2'):
    """
    Проверяем возможность добавления питомца с отрицательным возрастом. Ожидается код 400
    """

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем статус
    assert status == 400


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


@pytest.mark.put
@pytest.mark.skip(reason="Баг в продукте")
def test_unsuccessful_update_self_pet_info_with_empty_type(get_key, name='Кото пёс', animal_type=' ', age=3):
    """Обновление данных питомца: новая порода пустая строка. Ожидается ответ 400"""

    # Получаем ключ auth_key и список своих питомцев

    _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400
        assert status == 400

    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('Список питомцев пуст')


@pytest.mark.delete
@pytest.mark.skip(reason="Баг в продукте")
def test_unsuccessful_delete_another_user_pet(get_key):
    """Проверяем возможность удаления питомца другого пользователя. Ожидается отказ доступа"""

    # Получаем ключ auth_key и запрашиваем список всех питомцев

    _, all_pets = pf.get_list_of_pets(get_key, '')

    # Берём id первого питомца из общего списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][0]['id']
    status, _ = pf.delete_pet(get_key, pet_id)

    # Ещё раз запрашиваем список всех питомцев
    _, my_pets = pf.get_list_of_pets(get_key)

    # Проверяем что статус ответа не равен 200
    assert status != 200


@pytest.mark.post
@pytest.mark.skip(reason="Баг в продукте")
def test_add_new_pet_without_photo_empty_name(get_key, name='', animal_type='', age=''):
    """
    Простое добавление питомца (без фото) с пустым именем
    """

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем статус
    assert status != 200


@pytest.mark.post
@pytest.mark.skip(reason="Баг в продукте - <ссылка>")
def test_add_new_pet_without_photo_long_animal_type(get_key, name='Длиннопородный', age='1'):
    """
    Простое добавление питомца (без фото): порода - текст более 255 символов
    """

    # Добавляем питомца с длинным текстом в породе
    animal_type = 'Очень длинная порода testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttes' \
                  'ttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest' \
                  'testtesttesttesttesttesttesttesttesttesttesttesttesttesttest'

    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем статус
    assert status != 200
