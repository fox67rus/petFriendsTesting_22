# Позитивные тесты изменения данных питомцев
import pytest

from api import pf
import os
from config import generate_string, russian_chars, chinese_chars, special_chars


@pytest.mark.put
def test_successful_update_self_pet_info(get_key, name='Тыковка', animal_type='кошка', age='3'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем список питомцев пользователя
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Если список пустой, то добавляем питомца без фото для теста
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(get_key, name='Тест', animal_type='тест', age='1')
        _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Обновляем информацию питомца
    pet_id = my_pets['pets'][0]['id']
    status, result, response_headers = pf.update_pet_info(get_key, pet_id, name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert response_headers['Content-Type'] == 'application/json' or 'application/xml'


@pytest.mark.put
@pytest.mark.parametrize('pet_photo', [
    'images/dog.jpg',
    'images/mini-dog.png',
], ids=[
    'jpg photo',
    'png photo'
])
def test_successful_add_pets_correct_photo(get_key, pet_photo):
    """
    Проверяем, что можно добавить фото питомцу с корректным файлом изображения jpg или png
    """
    # Получаем полный путь к файлу с изображением питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Если список пустой, то добавляем питомца без фото для теста
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(get_key, name='Дуся', animal_type='хаски', age='1')
        _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result, response_headers = pf.add_pets_photo(get_key, pet_photo, pet_id)

    # Проверяем что статус ответа = 200 и у питомца есть фото
    assert status == 200
    assert 'data:image/' in result['pet_photo']
    assert response_headers['Content-Type'] == 'application/json' or 'application/xml'


@pytest.mark.put
@pytest.mark.parametrize("name", [
    generate_string(255),
    generate_string(1001),
    russian_chars(),
    russian_chars().upper(),
    chinese_chars(),
    special_chars(),
    '123',
    ''
], ids=[
    'name=255 symbols',
    'name=more than 1000 symbols',
    'name=russian',
    'name=RUSSIAN',
    'name=chinese',
    'name=specials',
    'name=digit',
    'name=empty'
])
@pytest.mark.parametrize("animal_type", [
    generate_string(255),
    generate_string(1001),
    russian_chars(),
    russian_chars().upper(),
    chinese_chars(),
    special_chars(),
    '123',
    ''
], ids=[
    'animal_type=255 symbols',
    'animal_type=more than 1000 symbols',
    'animal_type=russian',
    'animal_type=RUSSIAN',
    'animal_type=chinese',
    'animal_type=specials',
    'animal_type=digit',
    'animal_type=empty'
])
@pytest.mark.parametrize("age", [
    '0',
    '1',
    '50'
], ids=[
    'age=zero',
    'age=min',
    'age=max'
])
def test_successful_update_pet_info(get_key, delete_test_pets, name, animal_type, age):
    """
    Проверяем метод обновления данных питомца с различными допустимыми значениями.
    Тестовые данные после прохождения тестирования удаляются с помощью фикстуры.
    """

    # Получаем список питомцев пользователя
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Если список пустой, то добавляем питомца без фото для теста
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(get_key, name='Тест', animal_type='тест', age='1')
        _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Обновляем информацию питомца
    pet_id = my_pets['pets'][0]['id']
    status, result, response_headers = pf.update_pet_info(get_key, pet_id, name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert response_headers['Content-Type'] == 'application/json' or 'application/xml'
