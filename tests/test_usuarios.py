import requests
import uuid

BASE_URL = "https://serverest.dev"


def unique_email():
    """Generate a unique email to avoid conflicts."""
    return f"test_{uuid.uuid4().hex[:8]}@qa.com"


class TestUsuarios:

    def test_list_users(self):
        """TC-008 - List all registered users returns 200."""
        response = requests.get(f"{BASE_URL}/usuarios")
        assert response.status_code == 200
        assert "usuarios" in response.json()
        assert "quantidade" in response.json()

    def test_filter_users_by_name(self):
        """TC-009 - Filter users by name returns 200."""
        response = requests.get(f"{BASE_URL}/usuarios", params={"nome": "Fulano"})
        assert response.status_code == 200
        assert "usuarios" in response.json()

    def test_filter_users_by_email(self):
        """TC-010 - Filter users by email returns 200."""
        response = requests.get(f"{BASE_URL}/usuarios",
                                params={"email": "fulano@qa.com"})
        assert response.status_code == 200

    def test_filter_admin_users(self):
        """TC-011 - Filter admin users returns 200."""
        response = requests.get(f"{BASE_URL}/usuarios",
                                params={"administrador": "true"})
        assert response.status_code == 200

    def test_create_user_success(self):
        """TC-012 - Register a new user successfully returns 201."""
        email = unique_email()
        response = requests.post(f"{BASE_URL}/usuarios", json={
            "nome": "Test User Gislaine",
            "email": email,
            "password": "teste123",
            "administrador": "false"
        })
        assert response.status_code == 201
        assert "_id" in response.json()

    def test_create_user_duplicate_email(self):
        """TC-013 - Register user with duplicate email returns 400."""
        response = requests.post(f"{BASE_URL}/usuarios", json={
            "nome": "Test User",
            "email": "fulano@qa.com",
            "password": "teste",
            "administrador": "false"
        })
        assert response.status_code == 400

    def test_create_user_missing_fields(self):
        """TC-014 - Register user with missing fields returns 400."""
        response = requests.post(f"{BASE_URL}/usuarios", json={
            "nome": "Test User"
        })
        assert response.status_code == 400

    def test_create_user_invalid_email_format(self):
        """TC-015 - Register user with invalid email format returns 400."""
        response = requests.post(f"{BASE_URL}/usuarios", json={
            "nome": "Test User",
            "email": "invalidemail",
            "password": "teste",
            "administrador": "false"
        })
        assert response.status_code == 400

    def test_get_user_by_valid_id(self):
        """TC-016 - Get user by valid ID returns 200."""
        # First create a user to get a valid ID
        email = unique_email()
        create = requests.post(f"{BASE_URL}/usuarios", json={
            "nome": "Test User Gislaine",
            "email": email,
            "password": "teste123",
            "administrador": "false"
        })
        user_id = create.json()["_id"]

        response = requests.get(f"{BASE_URL}/usuarios/{user_id}")
        assert response.status_code == 200
        assert response.json()["email"] == email

    def test_get_user_invalid_id(self):
        """TC-017 - Get user with non-existent ID returns 400."""
        response = requests.get(f"{BASE_URL}/usuarios/invalidid123")
        assert response.status_code == 400

    def test_update_user(self):
        """TC-018 - Update existing user data returns 200."""
        email = unique_email()
        create = requests.post(f"{BASE_URL}/usuarios", json={
            "nome": "Original Name",
            "email": email,
            "password": "teste123",
            "administrador": "false"
        })
        user_id = create.json()["_id"]

        response = requests.put(f"{BASE_URL}/usuarios/{user_id}", json={
            "nome": "Updated Name",
            "email": unique_email(),
            "password": "newpass123",
            "administrador": "false"
        })
        assert response.status_code == 200

    def test_delete_user_success(self):
        """TC-019 - Delete user without active cart returns 200."""
        email = unique_email()
        create = requests.post(f"{BASE_URL}/usuarios", json={
            "nome": "User To Delete",
            "email": email,
            "password": "teste123",
            "administrador": "false"
        })
        user_id = create.json()["_id"]

        response = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
        assert response.status_code == 200

    def test_delete_nonexistent_user(self):
        """TC-020 - Delete non-existent user returns 200 with message."""
        response = requests.delete(f"{BASE_URL}/usuarios/invalidid123")
        assert response.status_code == 200
