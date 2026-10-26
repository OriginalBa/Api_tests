import pytest


@pytest.fixture(scope="session")
def base_url():
    return "https://book-club.qa.guru/api/v1"
