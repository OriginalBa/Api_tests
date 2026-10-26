import requests
import pytest
from jsonschema import validate
from schema.club_schemas import clubs_list_schema, club_schema, review_schema

BASE_URL = "https://book-club.qa.guru/api/v1"


def test_1_clubs_list_schema_validation():
    response = requests.get(f"{BASE_URL}/clubs/")
    assert response.status_code == 200, f"Ожидался 200 OK, но сервер вернул {response.status_code}"

    response_json = response.json()

    validate(instance=response_json, schema=clubs_list_schema)


def test_2_single_club_schema_validation():
    list_response = requests.get(f"{BASE_URL}/clubs/")
    assert list_response.status_code == 200

    clubs = list_response.json().get("results", [])
    if not clubs:
        pytest.skip("Список клубов пуст на сервере, пропускаем тест проверки отдельного клуба")

    target_club_id = clubs[0]["id"]

    response = requests.get(f"{BASE_URL}/clubs/{target_club_id}/")
    assert response.status_code == 200, f"Не удалось открыть клуб с ID {target_club_id}"

    response_json = response.json()

    validate(instance=response_json, schema=club_schema)


def test_3_all_embedded_reviews_schema_validation():
    response = requests.get(f"{BASE_URL}/clubs/")
    assert response.status_code == 200

    clubs = response.json().get("results", [])

    review_checked = False
    for club in clubs:
        for review in club.get("reviews", []):
            validate(instance=review, schema=review_schema)
            review_checked = True

    if not review_checked:
        pytest.skip("На первой странице ни у одного клуба не нашлось отзывов для валидации")


@pytest.mark.parametrize("field", ["count", "next", "previous", "results"])
def test_4_clubs_list_required_fields(field):
    response = requests.get(f"{BASE_URL}/clubs/")
    assert response.status_code == 200

    response_json = response.json()
    assert field in response_json, f"Обязательное поле '{field}' отсутствует в корне ответа API"


def test_5_club_types_and_formats_validation():
    response = requests.get(f"{BASE_URL}/clubs/")
    assert response.status_code == 200

    clubs = response.json().get("results", [])
    if not clubs:
        pytest.skip("Список клубов пуст, невозможно проверить типы полей элемента")

    first_club = clubs[0]

    assert isinstance(first_club["id"], int), "Поле 'id' должно быть целым числом"
    assert isinstance(first_club["bookTitle"], str), "Поле 'bookTitle' должно быть строкой"
    assert isinstance(first_club["members"], list), "Поле 'members' должно быть массивом (list)"
    assert isinstance(first_club["reviews"], list), "Поле 'reviews' должно быть массивом (list)"
