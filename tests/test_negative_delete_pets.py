# Негативные тесты удаления питомцев
import pytest

from api import pf


@pytest.mark.skip(reason="Баг в продукте - https://petfriends.skillfactory.ru/my_pets")
@pytest.mark.negative
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
