import requests

BASE_URL = "https://serverest.dev"


class TestLogin:

    def test_login_success(self):
        """TC-001 - Successful login with valid credentials."""
        response = requests.post(f"{BASE_URL}/login", json={
            "email": "fulano@qa.com",
            "password": "teste"
        })
        assert response.status_code == 200
        assert "authorization" in response.json()
        assert response.json()["message"] == "Login realizado com sucesso"

    def test_login_invalid_password(self):
        """TC-002 - Login with invalid password returns 401."""
        response = requests.post(f"{BASE_URL}/login", json={
            "email": "fulano@qa.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_nonexistent_email(self):
        """TC-003 - Login with non-existent email returns 401."""
        response = requests.post(f"{BASE_URL}/login", json={
            "email": "notexist@qa.com",
            "password": "teste"
        })
        assert response.status_code == 401

    def test_login_missing_email(self):
        """TC-004 - Login with missing email field returns 400."""
        response = requests.post(f"{BASE_URL}/login", json={
            "password": "teste"
        })
        assert response.status_code == 400

    def test_login_missing_password(self):
        """TC-005 - Login with missing password field returns 400."""
        response = requests.post(f"{BASE_URL}/login", json={
            "email": "fulano@qa.com"
        })
        assert response.status_code == 400

    def test_login_empty_body(self):
        """TC-006 - Login with empty body returns 400."""
        response = requests.post(f"{BASE_URL}/login", json={})
        assert response.status_code == 400

    def test_login_invalid_email_format(self):
        """TC-007 - Login with invalid email format returns 400."""
        response = requests.post(f"{BASE_URL}/login", json={
            "email": "notanemail",
            "password": "teste"
        })
        assert response.status_code == 400
