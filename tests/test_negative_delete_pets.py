# Негативные тесты удаления питомцев
import pytest

from api import pf
from config import generate_string, russian_chars, chinese_chars, special_chars


@pytest.mark.skip(reason="Баг в продукте - удаляется питомец другого пользователя")
@pytest.mark.delete
def test_unsuccessful_delete_another_user_pet(get_key):
    """Проверяем возможность удаления питомца другого пользователя. Ожидается отказ доступа"""

    # Получаем список всех питомцев на сайте
    _, all_pets, _ = pf.get_list_of_pets(get_key)

    # Берём id первого питомца из общего списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][0]['id']
    status, _, _ = pf.delete_pet(get_key, pet_id)
    # Ещё раз запрашиваем список всех питомцев
    _, all_pets, _ = pf.get_list_of_pets(get_key)

    # Проверяем статус ответа и что выбранный питомец не удалён
    assert status == 400
    assert pet_id in all_pets


@pytest.mark.parametrize("invalid_auth_key",
                         [
                             '',
                             '123',
                             generate_string(255),
                             generate_string(1001),
                             russian_chars(),
                             russian_chars().upper(),
                             chinese_chars(),
                             special_chars()
                         ], ids=[
                            'key=empty',
                            'key=digit',
                            'key=string 255',
                            'key=string 1001',
                            'key=russian',
                            'key=RUSSIAN',
                            'key=chinese',
                            'key=specials'])
def test_delete_pet_invalid_key(get_key, invalid_auth_key):
    """Проверяем возможность удаления питомца с некорректным ключом авторизации. Ожидается ответ 403"""

    # Получаем список питомцев пользователя
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(get_key, 'Тестик', 'кот', '2')
        _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление с некорректным ключом
    pet_id = my_pets['pets'][0]['id']
    status, _, _ = pf.delete_pet(invalid_auth_key, pet_id)

    # Проверяем статус ответа
    assert status == 403


@pytest.mark.parametrize("invalid_pet_id",
                         [
                             '',
                             '123',
                             generate_string(255),
                             generate_string(1001),
                             russian_chars(),
                             russian_chars().upper(),
                             chinese_chars(),
                             special_chars()
                         ], ids=[
                            'pet_id=empty',
                            'pet_id=digit',
                            'pet_id=string 255',
                            'pet_id=string 1001',
                            'pet_id=russian',
                            'pet_id=RUSSIAN',
                            'pet_id=chinese',
                            'pet_id=specials'])
def test_delete_pet_invalid_key(get_key, invalid_pet_id):
    """Проверяем возможность удаления питомца с не корректным pet_id."""

    # Получаем список питомцев пользователя
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(get_key, 'Тестик', 'кот', '2')
        _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Отправляем запрос на удаление с не корректным pet_id
    status, _, _ = pf.delete_pet(get_key, invalid_pet_id)

    # Проверяем статус ответа
    assert status == 404
