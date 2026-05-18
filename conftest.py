import pytest
import requests

BASE_URL = "https://serverest.dev"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_token():
    """Login and return the authorization token for the session."""
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "fulano@qa.com",
        "password": "teste"
    })
    assert response.status_code == 200, "Failed to obtain auth token"
    return response.json()["authorization"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    """Return headers with authorization token."""
    return {"Authorization": auth_token}
