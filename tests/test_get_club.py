import requests

from jsonschema import validate
from schema.get_club_schemas import get_clubs_schema


def test_total_count_with_schema_validation():
    response = requests.get("https://book-club.qa.guru/api/v1/clubs/")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    total_count = body["count"]

    response_all = requests.get("https://book-club.qa.guru/api/v1/clubs/", params={"page_size": total_count})

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response_all.status_code == 200

    body_all = response_all.json()
    validate(body_all, schema=get_clubs_schema)
    assert body_all["count"] >= len(body_all["results"])


def test_page_size_clubs():
    payload = {"page_size": 2}
    response = requests.get("https://book-club.qa.guru/api/v1/clubs/", params=payload)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()

    assert len(body["results"]) == payload["page_size"]


def test_search_clubs():
    payload = {"search": "Club The Wealth of Nations"}
    response = requests.get("https://book-club.qa.guru/api/v1/clubs/", params=payload)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    clubs = body.get("results", [])

    assert body["count"] > 0, f"По запросу '{payload['search']}' ничего не найдено"
    assert len(clubs) > 0, "Массив результатов пуст"
    for club in clubs:
        assert payload["search"] in club["bookTitle"], \
            f"Строка поиска '{payload['search']}' не найдена в названии книги '{club['bookTitle']}'"
