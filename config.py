import functools

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


def log_test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        status = str(response[0])
        result = str(response[1])
        request_headers = str(response[2])
        response_headers = str(response[3])
        with open('log.txt', 'a', encoding='utf8') as f:
            f.write(f'{func.__name__}\n'
                    f'{func.__doc__}\n'
                    f'Запрос:\n'
                    f'------------------\n'
                    f'Заголовки запроса: {request_headers}\n'
                    f'Параметры пути:\n'
                    f'Параметры строки:\n'
                    f'Тело запроса:\n\n'
                    f'------------------\n'
                    f'Ответ:\n'
                    f'------------------\n'
                    f'Код ответа: {status}\n'
                    f'Тело ответа:\n'
                    f'{result}\n'
                    f'Заголовки ответа:\n'
                    f'{response_headers}\n'
                    f'===================\n\n')
    return wrapper
