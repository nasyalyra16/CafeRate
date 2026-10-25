import pytest
from fastapi.testclient import TestClient
from main import app
from app.repositories import memory


@pytest.fixture(autouse=True)
def clean_store():
    memory.reset_store()
    yield
    memory.reset_store()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {"X-API-Key": "caferate-dev-key"}


@pytest.fixture
def cafe_payload():
    return {
        "name": "Kopi Sudut",
        "area": "Samata",
        "address": "Jl. H.M. Yasin Limpo",
        "category": "Coffee Shop",
    }


@pytest.fixture
def review_payload():
    return {
        "visitor_alias": "PengunjungA",
        "service_rating": 5,
        "taste_rating": 4,
        "ambience_rating": 5,
        "comment": "Pelayanan ramah dan tempat nyaman.",
    }
