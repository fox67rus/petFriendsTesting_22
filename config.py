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
        response_headers = str(response[2])
        with open('log.txt', 'w', encoding='utf8') as f:
            f.write(f'''Запрос:
                        ------------------
                        Заголовки запроса:
                        Параметры пути: 
                        Параметры строки:
                        Тело запроса:                      

                        Ответ:
                        ------------------
                        Код ответа: {status}
                        Тело ответа:
                        {result}
                        Заголовки ответа:
                        {response_headers}
                    ''')
    return wrapper
