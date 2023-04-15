# Позитивные тесты добавления питомцев
import pytest

from api import pf
import os

from config import generate_string, russian_chars, chinese_chars, special_chars


@pytest.mark.post
def test_add_new_pet_with_valid_data(get_key, name='Рыжик', animal_type='кот',
                                     age='2', pet_photo='images/red.jpg'):
    """
    Проверяем что можно добавить питомца с корректными данными
    """
    # Получаем полный путь к файлу с изображением питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result, response_headers = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    # Сверяем статус и результат
    assert status == 200
    assert result['name'] == name
    assert response_headers['Content-Type'] == 'application/json' or 'application/xml'


@pytest.mark.post
def test_add_new_pet_without_photo_valid_data(get_key, name='Снежок', animal_type='хаски', age='0'):
    """
    Проверяем простой метод добавления питомца с корректными данными
    """

    # Добавляем питомца
    status, result, response_headers = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем статус и результат
    assert status == 200
    assert result['name'] == name
    assert response_headers['Content-Type'] == 'application/json' or 'application/xml'


@pytest.mark.post
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
    'name = 255 symbols',
    'name = more than 1000 symbols',
    'name = russian',
    'name = RUSSIAN',
    'name = chinese',
    'name = specials',
    'name = digit',
    'name = empty'
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
    'animal_type = 255 symbols',
    'animal_type = more than 1000 symbols',
    'animal_type = russian',
    'animal_type = RUSSIAN',
    'animal_type = chinese',
    'animal_type = specials',
    'animal_type = digit',
    'animal_type = empty'
])
@pytest.mark.parametrize("age", [
    '0',
    '1',
    '50'
    ], ids=[
    'age = zero',
    'age = min',
    'age = max'
])
def test_add_new_pet_simple(get_key, delete_test_pets, name, animal_type, age):
    """
    Проверяем простой метод добавления питомца с различными допустимыми значениями параметрами.
    Тестовые данные после прохождения тестирования удаляются с помощью фикстуры.
    """

    # Добавляем питомца
    status, result, response_headers = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем статус и результат
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert response_headers['Content-Type'] == 'application/json' or 'application/xml'

