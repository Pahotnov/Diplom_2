import allure
import requests

from urls import Urls


class TestCreateOrder:

    @allure.title("Проверка создания заказа с ингредиентом авторизованным пользователем")
    @allure.description("Пользователь может авторизоваться и создать заказ с ингредиентом - успешный запрос возвращает имя и email пользователя")
    def test_success_authorized_create_order_with_ingredient(self, create_new_user_and_return_email_password, get_ingredients):
        login_pass_data = create_new_user_and_return_email_password
        ingredients = get_ingredients
        payload = {
            "email": login_pass_data[0],
            "password": login_pass_data[1],
            "name": login_pass_data[2]
        }
        email = payload['email']
        name = payload['name']
        response = requests.post(Urls.LOGIN_USER_URL, data=payload)
        access_token = response.json()['accessToken']
        response = requests.post(Urls.ORDERS_URL, headers={'Authorization': access_token}, data=ingredients)
        assert response.status_code == 200
        assert '"success":true' in response.text
        assert '"owner"' in response.text
        assert f'"name":"{name}","email":"{email}"' in response.text

    @allure.title("Проверка создания заказа с ингредиентом неавторизованным пользователем")
    @allure.description("Пользователь не может авторизоваться, запрос возвращает ошибку. Заказ невозможно создать без авторизации")
    def test_success_unauthorized_create_order_with_ingredient(self, get_ingredients):
        ingredients = get_ingredients
        response = requests.post(Urls.ORDERS_URL, data=ingredients)
        assert response.status_code == 200
        assert '"success":true' in response.text
        assert '"owner"' not in response.text

    @allure.title("Проверка создания заказа без ингредиентов авторизованным пользователем")
    @allure.description("Пользователь может авторизоваться, но не может создать заказ без ингредиентов - запрос возвращает ошибку")
    def test_unsuccess_authorized_create_order_without_ingredient(self, create_new_user_and_return_email_password):
        login_pass_data = create_new_user_and_return_email_password
        payload = {
            "email": login_pass_data[0],
            "password": login_pass_data[1],
            "name": login_pass_data[2]
        }
        response = requests.post(Urls.LOGIN_USER_URL, data=payload)
        access_token = response.json()['accessToken']
        response = requests.post(Urls.ORDERS_URL, headers={'Authorization': access_token})
        assert response.status_code == 400
        assert response.text == '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title("Проверка создания заказа без ингредиента неавторизованным пользователем")
    @allure.description("Пользователь не может авторизоваться и создать заказ с ингредиентом - запрос возвращает ошибку")
    def test_unsuccess_unauthorized_create_order_without_ingredient(self):
        response = requests.post(Urls.ORDERS_URL)
        assert response.status_code == 400
        assert response.text == '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title("Проверка создания заказа с ингредиентом, у которого неверный хэш, авторизованным пользователем")
    @allure.description("Пользователь может авторизоваться, но не может создать заказ - запрос возвращает ошибку")
    def test_unsuccess_authorized_create_order_with_uncorrect_ingredient_hash(self, create_new_user_and_return_email_password, get_ingredients):
        login_pass_data = create_new_user_and_return_email_password
        ingredients = {'ingredients': 'test'}
        payload = {
            "email": login_pass_data[0],
            "password": login_pass_data[1],
            "name": login_pass_data[2]
        }
        response = requests.post(Urls.LOGIN_USER_URL, data=payload)
        access_token = response.json()['accessToken']
        response = requests.post(Urls.ORDERS_URL, headers={'Authorization': access_token}, data=ingredients)
        assert response.status_code == 500
        assert 'Error' in response.text

    @allure.title("Проверка создания заказа с ингредиентом, у которого неверный хэш, неавторизованным пользователем")
    @allure.description("Пользователь не может авторизоваться и создать заказ с ингредиентом, у которого неверный хэш - запрос возвращает ошибку")
    def test_unsuccess_unauthorized_create_order_with_uncorrect_ingredient_hash(self, get_ingredients):
        ingredients = {'ingredients': 'test'}
        response = requests.post(Urls.ORDERS_URL, data=ingredients)
        assert response.status_code == 500
        assert 'Error' in response.text
