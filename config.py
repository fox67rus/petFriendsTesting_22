valid_email = 'test@qiott.com'
valid_password = 'Qwerty_123'

invalid_email = 'test@qiott123.com'
invalid_password = 'some_password'


def generate_string(n: int) -> str:
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'
