import allure
import pytest

from helpers import generate_random_string, generate_random_email

import requests

from urls import Urls


class TestCreateUser:

    @allure.title("Проверка создания уникального пользователя")
    @allure.description("Проверка того, что пользователя можно создать;"
                        " запрос возвращает правильный код ответа;"
                        " успешный запрос возвращает {\"success\":true}")
    def test_create_new_user_correct_status_and_answer(self):
        email = generate_random_email(8)
        password = generate_random_string(8)
        name = generate_random_string(8)

        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        response = requests.post(Urls.CREATE_USER_URL, data=payload)
        access_token = response.json()['accessToken']
        requests.delete(Urls.GET_USER_DATA_URL, headers={'Authorization': access_token})
        assert response.status_code == 200
        assert '"success":true' in response.text

    @allure.title("Проверка создания уже зарегистрированного пользователя")
    @allure.description("Проверка того, что нельзя создать двух одинаковых пользователей;"
                        " если создать пользователя с email, который уже есть, возвращается ошибка")
    def test_create_new_user_twice(self):
        email = generate_random_email(8)
        password = generate_random_string(8)
        name = generate_random_string(8)

        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        first_response = requests.post(Urls.CREATE_USER_URL, data=payload)
        second_response = requests.post(Urls.CREATE_USER_URL, data=payload)
        assert second_response.status_code == 403
        assert second_response.text == '{"success":false,"message":"User already exists"}'
        access_token = first_response.json()['accessToken']
        requests.delete(Urls.GET_USER_DATA_URL, headers={'Authorization': access_token})

    @allure.title("Создание пользователя без одного из обязательных полей")
    @allure.description("Проверка того, что нельзя создать нового пользователя без обязательных полей;"
                        " если одного из полей нет, запрос возвращает ошибку")
    @pytest.mark.parametrize('email, password', [[generate_random_email(8), ''], ['', 'password12345']])
    def test_create_new_user_without_obligatory_fields(self, email, password):
        payload = {
            "email": email,
            "password": password,
            "name": "TestName"
        }

        response = requests.post(Urls.CREATE_USER_URL, data=payload)
        assert response.status_code == 403
        assert response.text == '{"success":false,"message":"Email, password and name are required fields"}'
