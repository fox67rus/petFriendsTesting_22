# Позитивные тесты добавления питомцев
import pytest

from api import pf
import os


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
