import string
import random

import allure


@allure.title("Генерация случайных пароля и имени")
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@allure.title("Генерация случайного email")
def generate_random_email(length):
    email = generate_random_string(length)
    email += '@test.test'
    return email
