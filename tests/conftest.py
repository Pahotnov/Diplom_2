import pytest
import requests

from helpers import generate_random_string, generate_random_email
from urls import Urls


@pytest.fixture
def create_new_user_and_return_email_password():
    login_pass = []

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

    if response.status_code == 200:
        login_pass.append(email)
        login_pass.append(password)
        login_pass.append(name)

    yield login_pass
    requests.delete(Urls.GET_USER_DATA_URL, headers={'Authorization': access_token})


@pytest.fixture
def get_ingredients():
    ingredients = {'ingredients': [requests.get(Urls.GET_INGREDIENTS_URL).json()['data'][0]['_id']]}
    return ingredients
