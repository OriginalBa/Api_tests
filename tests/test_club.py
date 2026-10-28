import requests
import random
from jsonschema import validate

from schema.club_schemas import success_create_club

API_URL = "https://book-club.qa.guru/api/v1"
USERNAME = "user_roman1"
PASSWORD = "user_roman11"
USERNAME_ID = 10701


def test_success_create_club():
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    access_token = auth_response.json()["access"]

    book_title = f"title Rkhalimov {random.randint(1000, 999999)}"
    book_author = f"author Rkhalimov"
    club_body = {
        "bookTitle": book_title,
        "bookAuthors": book_author,
        "publicationYear": 2026,
        "description": "Вот такая книжка, ребята",
        "telegramChatLink": "https://t.me/qa.guru"
    }
    club_headers = {"Authorization": "Bearer " + access_token}
    club_response = requests.post(API_URL + "/clubs/", headers=club_headers, json=club_body)

    print("\nStatus code:", club_response.status_code)
    print("Headers:", club_response.headers)
    print("Body:", club_response.text)

    assert club_response.status_code == 201

    club_response_body = club_response.json()
    validate(club_response_body, schema=success_create_club)

    assert club_response_body["bookTitle"] == book_title
    assert club_response_body["bookAuthors"] == book_author
    assert club_response_body["publicationYear"] == club_body["publicationYear"]
    assert club_response_body["description"] == club_body["description"]
    assert club_response_body["telegramChatLink"] == club_body["telegramChatLink"]
    assert club_response_body["owner"] == USERNAME_ID
    assert USERNAME_ID in club_response_body["members"]
    assert len(club_response_body["reviews"]) == 0
    assert club_response_body["modified"] is None

    club_id = club_response_body["id"]
    delete_response = requests.delete(API_URL + f"/clubs/{club_id}/", headers=club_headers)
    assert delete_response.status_code is 204


def test_success_get_club():
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    access_token = auth_response.json()["access"]

    club_body = {
        "bookTitle": "title Rkhalimov",
        "bookAuthors": "author Rkhalimov",
        "publicationYear": 2026,
        "description": "Вот такая книжка, ребята",
        "telegramChatLink": "https://t.me/qa.guru"
    }
    club_headers = {"Authorization": "Bearer " + access_token}
    club_response = requests.post(API_URL + "/clubs/", headers=club_headers, json=club_body)

    print("\nStatus code:", club_response.status_code)
    print("Headers:", club_response.headers)
    print("Body:", club_response.text)

    assert club_response.status_code == 201

    club_response_body = club_response.json()
    club_id = club_response_body["id"]

    get_response = requests.get(API_URL + f"/clubs/{club_id}/", headers=club_headers)
    get_response_body = get_response.json()

    assert get_response_body["id"] == club_id
    assert get_response_body["bookTitle"] == club_body["bookTitle"]
    assert get_response_body["bookAuthors"] == club_body["bookAuthors"]
    assert get_response_body["publicationYear"] == club_body["publicationYear"]
    assert get_response_body["description"] == club_body["description"]
    assert get_response_body["telegramChatLink"] == club_body["telegramChatLink"]
    assert get_response_body["owner"] == USERNAME_ID

    delete_response = requests.delete(API_URL + f"/clubs/{club_id}/", headers=club_headers)
    assert delete_response.status_code is 204


def test_success_update_club():
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    access_token = auth_response.json()["access"]

    club_body = {
        "bookTitle": "title Rkhalimov",
        "bookAuthors": "author Rkhalimov",
        "publicationYear": 2026,
        "description": "Вот такая книжка, ребята",
        "telegramChatLink": "https://t.me/qa.guru"
    }
    club_headers = {"Authorization": "Bearer " + access_token}
    club_response = requests.post(API_URL + "/clubs/", headers=club_headers, json=club_body)

    print("\nStatus code:", club_response.status_code)
    print("Headers:", club_response.headers)
    print("Body:", club_response.text)

    assert club_response.status_code == 201

    club_response_body = club_response.json()
    club_id = club_response_body["id"]

    patch_club_body = {
        "bookTitle": "Another title Rkhalimov",
        "bookAuthors": "Another author Rkhalimov"
    }

    patch_response = requests.patch(API_URL + f"/clubs/{club_id}/", headers=club_headers, json=patch_club_body)
    assert patch_response.status_code == 200

    patch_response_body = patch_response.json()

    assert patch_response_body["bookTitle"] == patch_club_body["bookTitle"]
    assert patch_response_body["bookAuthors"] == patch_club_body["bookAuthors"]
    assert patch_response_body["modified"] is not None

    delete_response = requests.delete(API_URL + f"/clubs/{club_id}/", headers=club_headers)
    assert delete_response.status_code is 204


def test_success_delete_club():
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    access_token = auth_response.json()["access"]

    club_body = {
        "bookTitle": "title Rkhalimov",
        "bookAuthors": "author Rkhalimov",
        "publicationYear": 2026,
        "description": "Вот такая книжка, ребята",
        "telegramChatLink": "https://t.me/qa.guru"
    }
    club_headers = {"Authorization": "Bearer " + access_token}
    club_response = requests.post(API_URL + "/clubs/", headers=club_headers, json=club_body)

    print("\nStatus code:", club_response.status_code)
    print("Headers:", club_response.headers)
    print("Body:", club_response.text)

    assert club_response.status_code == 201

    club_response_body = club_response.json()
    club_id = club_response_body["id"]

    delete_response = requests.delete(API_URL + f"/clubs/{club_id}/", headers=club_headers)
    assert delete_response.status_code is 204
