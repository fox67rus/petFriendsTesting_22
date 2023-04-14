import pytest
from tests.test_pet_friends import pf, valid_password, valid_email


@pytest.fixture()
def get_key():
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    status, key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in key
    return key
