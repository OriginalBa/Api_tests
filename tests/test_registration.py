import requests

from jsonschema import validate
from schema.reg_schemas import registration_schema

API_URL = "https://book-club.qa.guru/api/v1"
USERNAME = "registration_fail"
PASSWORD = "password"


def test_successful_registration():
    request_body = {"username": USERNAME, "password": PASSWORD}

    response = requests.post(f"{API_URL}/users/register/", json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 201

    body = response.json()
    validate(body, schema=registration_schema)

    assert body["username"] == request_body["username"]

    response_auth_token = requests.post(f"{API_URL}/auth/token/", json=request_body)

    auth_token_body = response_auth_token.json()
    auth_token = auth_token_body["access"]

    response_delete_user = requests.delete(f"{API_URL}/users/me/", headers={"Authorization": "Bearer " + auth_token})
    assert response_delete_user.status_code is 204
