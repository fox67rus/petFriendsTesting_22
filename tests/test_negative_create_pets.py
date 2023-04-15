# Негативные тесты добавления питомцев
import pytest

from api import pf
import os


@pytest.mark.skip(reason="Баг в продукте - https://petfriends.skillfactory.ru/my_pets")
@pytest.mark.post
@pytest.mark.negative
def test_add_new_pet_without_photo_negative_data(get_key, name='Гав', animal_type='котёнок', age='-2'):
    """
    Проверяем возможность добавления питомца с отрицательным возрастом. Ожидается код 400
    """

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем статус
    assert status == 400


@pytest.mark.post
def test_add_new_pet_with_negative_data(log, get_key, name='Рыжик', animal_type='кот',
                                        age='2', pet_photo='images/red.gif'):
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
