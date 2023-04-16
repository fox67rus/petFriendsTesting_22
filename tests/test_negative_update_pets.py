# Негативные тесты изменения питомцев
import pytest

from api import pf


@pytest.mark.skip(reason="Баг в продукте - доступ к питомцам других пользователей")
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
