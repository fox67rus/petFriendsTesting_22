# Негативные тесты добавления питомцев
import pytest

from api import pf
import os
from config import generate_string, russian_chars, chinese_chars, special_chars


@pytest.mark.post
@pytest.mark.parametrize("name", [''], ids=['name=empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['animal_type=empty'])
@pytest.mark.parametrize("age",
                         [
                             '',
                             '-1',
                             '100',
                             '1.5',
                             '2147483647',
                             '2147483648',
                             russian_chars(),
                             russian_chars().upper(),
                             chinese_chars(),
                             special_chars()
                         ], ids=[
                            'age=empty',
                            'age=negative',
                            'age=over max',
                            'age=float',
                            'age=max integer',
                            'age=over max integer',
                            'age=russian',
                            'age=RUSSIAN',
                            'age=chinese',
                            'age=specials'])
def test_add_new_pet_without_photo_negative_data(get_key, delete_test_pets, name, animal_type, age):
    """
    Проверяем возможность добавления питомца с отрицательным возрастом. Ожидается код 400
    """

    # Добавляем питомца
    status, _, _ = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Сверяем статус
    assert status == 400


@pytest.mark.post
@pytest.mark.parametrize("name", [''], ids=['name=empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['animal_type=empty'])
@pytest.mark.parametrize("age", [''], ids=['age=empty'])
@pytest.mark.parametrize("pet_photo",
                         [
                             'images/mini-dog.gif',
                             'images/photo.txt',
                             generate_string(10),
                             russian_chars(),
                             special_chars(),
                             '123',
                             ''
                         ], ids=[
                             'pet_photo=gif file',
                             'pet_photo=txt file',
                             'pet_photo=english text',
                             'pet_photo=russian text',
                             'pet_photo=special chars',
                             'pet_photo=numbers',
                             'pet_photo=empty'
                         ])
def test_add_new_pet_negative_data(get_key, delete_test_pets, name, animal_type, age, pet_photo):
    """
    Проверяем метод добавления питомцев с различными недопустимыми значениями.
    Тестовые данные после прохождения тестирования удаляются с помощью фикстуры.
    """

    # Получаем полный путь к файлу с изображением питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, _, _ = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    # Сверяем статус
    assert status == 400
