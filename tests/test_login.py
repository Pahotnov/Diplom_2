import allure
import requests

from urls import Urls


class TestLoginUser:

    @allure.title("Проверка авторизации существующего пользователя")
    @allure.description("Пользователь может авторизоваться, успешный запрос возвращает токек доступа и данные пользователя")
    def test_success_user_login(self, create_new_user_and_return_email_password):
        login_pass_data = create_new_user_and_return_email_password
        payload = {
            "email": login_pass_data[0],
            "password": login_pass_data[1]
        }
        email = str(login_pass_data[0])
        response = requests.post(Urls.LOGIN_USER_URL, data=payload)
        assert response.status_code == 200
        assert '"success":true' in response.text
        assert f'"user":{{"email":"{email}"' in response.text

    @allure.title("Проверка авторизации несуществующего пользователя")
    @allure.description("Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_user_login_with_not_existing_data(self):
        payload = {
            "login": "Test",
            "password": "Test"
        }
        response = requests.post(Urls.LOGIN_USER_URL, data=payload)
        assert response.status_code == 401
        assert response.text == '{"success":false,"message":"email or password are incorrect"}'
