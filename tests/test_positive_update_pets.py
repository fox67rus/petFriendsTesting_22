# Позитивные тесты изменения данных питомцев
import pytest

from api import pf
import os


@pytest.mark.put
def test_successful_update_self_pet_info(get_key, name='Тыковка', animal_type='кошка', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем список питомцев пользователя
    _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('Список питомцев пуст')


@pytest.mark.put
def test_successful_add_pets_correct_photo(get_key, pet_photo='images/dog.jpg'):
    """
    Проверяем, что можно добавить фото питомцу с корректным файлом изображения
    """
    # Получаем полный путь к файлу с изображением питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем список своих питомцев
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
