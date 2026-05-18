import requests
import uuid

BASE_URL = "https://serverest.dev"


def unique_product_name():
    """Generate a unique product name to avoid conflicts."""
    return f"Test Product Gislaine {uuid.uuid4().hex[:8]}"


class TestProdutos:

    def test_list_products(self):
        """TC-021 - List all registered products returns 200."""
        response = requests.get(f"{BASE_URL}/produtos")
        assert response.status_code == 200
        assert "produtos" in response.json()
        assert "quantidade" in response.json()

    def test_filter_products_by_name(self):
        """TC-022 - Filter products by name returns 200."""
        response = requests.get(f"{BASE_URL}/produtos",
                                params={"nome": "Logitech MX"})
        assert response.status_code == 200
        assert "produtos" in response.json()

    def test_create_product_without_token(self):
        """TC-023 - Create product without token returns 401."""
        response = requests.post(f"{BASE_URL}/produtos", json={
            "nome": unique_product_name(),
            "preco": 100,
            "descricao": "Test product",
            "quantidade": 10
        })
        assert response.status_code == 401

    def test_create_product_with_token(self, auth_headers):
        """TC-024 - Create product with valid admin token returns 201."""
        response = requests.post(f"{BASE_URL}/produtos",
                                 headers=auth_headers,
                                 json={
                                     "nome": unique_product_name(),
                                     "preco": 1500,
                                     "descricao": "Notebook for testing purposes",
                                     "quantidade": 10
                                 })
        assert response.status_code == 201
        assert "_id" in response.json()

    def test_create_product_missing_fields(self, auth_headers):
        """TC-025 - Create product with missing fields returns 400."""
        response = requests.post(f"{BASE_URL}/produtos",
                                 headers=auth_headers,
                                 json={"nome": unique_product_name()})
        assert response.status_code == 400

    def test_get_product_by_valid_id(self, auth_headers):
        """TC-026 - Get product by valid ID returns 200."""
        # Create product first
        create = requests.post(f"{BASE_URL}/produtos",
                               headers=auth_headers,
                               json={
                                   "nome": unique_product_name(),
                                   "preco": 500,
                                   "descricao": "Test product",
                                   "quantidade": 5
                               })
        product_id = create.json()["_id"]

        response = requests.get(f"{BASE_URL}/produtos/{product_id}")
        assert response.status_code == 200
        assert response.json()["_id"] == product_id

    def test_get_product_invalid_id(self):
        """TC-027 - Get product with invalid ID returns 400."""
        response = requests.get(f"{BASE_URL}/produtos/invalidid123")
        assert response.status_code == 400

    def test_update_product(self, auth_headers):
        """TC-028 - Update product as admin returns 200."""
        create = requests.post(f"{BASE_URL}/produtos",
                               headers=auth_headers,
                               json={
                                   "nome": unique_product_name(),
                                   "preco": 200,
                                   "descricao": "Original description",
                                   "quantidade": 3
                               })
        product_id = create.json()["_id"]

        response = requests.put(f"{BASE_URL}/produtos/{product_id}",
                                headers=auth_headers,
                                json={
                                    "nome": unique_product_name(),
                                    "preco": 300,
                                    "descricao": "Updated description",
                                    "quantidade": 5
                                })
        assert response.status_code == 200

    def test_delete_product(self, auth_headers):
        """TC-029 - Delete product not in any cart returns 200."""
        create = requests.post(f"{BASE_URL}/produtos",
                               headers=auth_headers,
                               json={
                                   "nome": unique_product_name(),
                                   "preco": 100,
                                   "descricao": "Product to delete",
                                   "quantidade": 1
                               })
        product_id = create.json()["_id"]

        response = requests.delete(f"{BASE_URL}/produtos/{product_id}",
                                   headers=auth_headers)
        assert response.status_code == 200
