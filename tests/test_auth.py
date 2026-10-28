import requests
from jsonschema import validate

from schema.auth_schemas import success_auth, wrong_credentials_auth, unsupported_media_type, invalid_credentials_schema

API_URL = "https://book-club.qa.guru/api/v1/auth/token/"
USERNAME = "user_roman1"
PASSWORD = "user_roman11"
TOKEN_PATH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBl"


def test_successful_auth():
    request_body = {"username": USERNAME, "password": PASSWORD}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=success_auth)

    access_token = body["access"]
    refresh_token = body["refresh"]
    assert TOKEN_PATH in access_token
    assert TOKEN_PATH in refresh_token
    assert len(access_token.split(".")) == 3
    assert len(refresh_token.split(".")) == 3
    assert access_token != refresh_token


def test_wrong_credentials_auth():
    request_body = {"username": USERNAME, "password": "wrong"}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 401

    body = response.json()
    validate(body, schema=wrong_credentials_auth)

    assert body["detail"] == "Invalid username or password."


def test_missing_username_auth():
    request_body = {"password": PASSWORD}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["username"] == ["This field is required."]


def test_missing_password_auth():
    request_body = {"username": USERNAME}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["password"] == ["This field is required."]


def test_missing_username_and_password_auth():
    request_body = {}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["username"] == ["This field is required."]
    assert body["password"] == ["This field is required."]


def test_wrong_body_type_none():
    request_body = {"username": None, "password": None}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["username"] == ["This field may not be null."]
    assert body["password"] == ["This field may not be null."]


def test_wrong_body_type_boolean():
    request_body = {"username": True, "password": False}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["username"] == ["Not a valid string."]
    assert body["password"] == ["Not a valid string."]


def test_wrong_body_type_integer():
    request_body = {"username": 123, "password": 321}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 401

    body = response.json()
    validate(body, schema=wrong_credentials_auth)

    assert body["detail"] == "Invalid username or password."


def test_wrong_body_type_list():
    request_body = {"username": [], "password": []}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["username"] == ["Not a valid string."]
    assert body["password"] == ["Not a valid string."]


def test_wrong_content_type_auth():
    request_body = {"username": USERNAME, "password": PASSWORD}
    headers = {"content-type": "image/png"}

    response = requests.post(API_URL, headers=headers, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 415

    body = response.json()
    validate(body, schema=unsupported_media_type)

    assert body["detail"] == "Unsupported media type \"image/png\" in request."
