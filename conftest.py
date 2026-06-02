import pytest
import requests
from config import BASE_URL
from data.booking_data import AUTH_PAYLOAD

@pytest.fixture(scope="session")
def auth_headers():
    response = requests.post(f"{BASE_URL}/auth", json=AUTH_PAYLOAD)
    token = response.json()["token"]
    return {"Cookie": f"token={token}"}
