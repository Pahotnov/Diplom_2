import allure
import requests

from urls import Urls


class TestGetUserOrders:

    @allure.title("Проверка получения заказов авторизованным пользователем")
    @allure.description("Пользователь может авторизоваться, успешный запрос возвращает список заказов")
    def test_success_get_authorized_user_orders(self, create_new_user_and_return_email_password):
        login_pass_data = create_new_user_and_return_email_password
        payload = {
            "email": login_pass_data[0],
            "password": login_pass_data[1]
        }
        response = requests.post(Urls.LOGIN_USER_URL, data=payload)
        access_token = response.json()['accessToken']
        response = requests.get(Urls.ORDERS_URL, headers={'Authorization': access_token})
        assert response.status_code == 200
        assert '"success":true' in response.text
        assert 'orders' in response.text

    @allure.title("Проверка получения заказов неавторизованным пользователем")
    @allure.description("Пользователь не может авторизоваться и получить список заказов - запрос возвращает ошибку. Для получения заказов необходимо авторизоваться")
    def test_unsuccess_get_unauthorized_user_orders(self):
        response = requests.get(Urls.ORDERS_URL)
        assert response.status_code == 401
        assert '"success":false' in response.text
        assert '"message":"You should be authorised"' in response.text
