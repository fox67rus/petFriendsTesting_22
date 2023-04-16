# Позитивные тесты удаления питомцев
import pytest

from api import pf


@pytest.mark.delete
def test_successful_delete_self_pet(get_key):
    """Проверяем возможность удаления питомца"""

    # Получаем список питомцев пользователя
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(get_key, 'Кексик', 'кот', '2', 'images/red.jpg')
        _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _, response_headers = pf.delete_pet(get_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(get_key, 'my_pets')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    assert response_headers['Content-Type'] == 'application/json' or 'application/xml'
