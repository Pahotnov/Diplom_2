import allure
import requests

from helpers import generate_random_string, generate_random_email

from urls import Urls


class TestEditUserData:

    @allure.title("Проверка изменения данных авторизованным пользователем")
    @allure.description("Пользователь может авторизоваться и изменить данные, успешный запрос возвращает email и имя пользователя")
    def test_success_edit_authorized_user_data(self, create_new_user_and_return_email_password):
        login_pass_data = create_new_user_and_return_email_password
        payload = {
            "email": login_pass_data[0],
            "password": login_pass_data[1],
            "name": login_pass_data[2]
        }

        response = requests.post(Urls.LOGIN_USER_URL, data=payload)
        access_token = response.json()['accessToken']
        new_user_data = {
            "email": generate_random_email(8),
            "password": generate_random_string(8),
            "name": generate_random_string(8)
        }
        email = new_user_data['email']
        name = new_user_data['name']
        response = requests.patch(Urls.GET_USER_DATA_URL, headers={'Authorization': access_token}, data=new_user_data)
        assert response.status_code == 200
        assert '"success":true' in response.text
        assert f'"user":{{"email":"{email}","name":"{name}"}}}}' in response.text

    @allure.title("Проверка изменений данных неавторизованным пользователем")
    @allure.description("Пользователь не может авторизоваться, запрос возвращает ошибку. Изменить данные невозможно без авторизации")
    def test_unsuccess_edit_unathorized_user_data(self, create_new_user_and_return_email_password):
        login_pass_data = create_new_user_and_return_email_password
        payload = {
            "email": login_pass_data[0],
            "password": login_pass_data[1],
            "name": login_pass_data[2]
        }
        email = payload['email']
        name = payload['name']
        response = requests.post(Urls.LOGIN_USER_URL, data=payload)
        access_token = response.json()['accessToken']
        new_user_data = {
            "email": generate_random_email(8),
            "password": generate_random_string(8),
            "name": generate_random_string(8)
        }
        response = requests.get(Urls.GET_USER_DATA_URL, headers={'Authorization': access_token}, data=payload)
        assert response.text == f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}}}}'

        response = requests.patch(Urls.GET_USER_DATA_URL, data=new_user_data)
        assert response.status_code == 401
        assert '"success":false' in response.text
        assert '"message":"You should be authorised"' in response.text
