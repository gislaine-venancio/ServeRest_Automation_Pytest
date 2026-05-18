import requests
import uuid

BASE_URL = "https://serverest.dev"


def create_user_and_login():
    """Create a fresh user and return their token and ID."""
    email = f"cart_user_{uuid.uuid4().hex[:8]}@qa.com"
    create = requests.post(f"{BASE_URL}/usuarios", json={
        "nome": "Cart Test User",
        "email": email,
        "password": "teste123",
        "administrador": "false"
    })
    user_id = create.json()["_id"]

    login = requests.post(f"{BASE_URL}/login", json={
        "email": email,
        "password": "teste123"
    })
    token = login.json()["authorization"]
    return {"token": token, "user_id": user_id, "headers": {"Authorization": token}}


def create_product(auth_headers):
    """Create a product and return its ID."""
    name = f"Cart Product {uuid.uuid4().hex[:8]}"
    response = requests.post(f"{BASE_URL}/produtos",
                             headers=auth_headers,
                             json={
                                 "nome": name,
                                 "preco": 100,
                                 "descricao": "Product for cart testing",
                                 "quantidade": 50
                             })
    return response.json()["_id"]


class TestCarrinhos:

    def test_list_carts(self):
        """TC-030 - List all registered carts returns 200."""
        response = requests.get(f"{BASE_URL}/carrinhos")
        assert response.status_code == 200
        assert "carrinhos" in response.json()
        assert "quantidade" in response.json()

    def test_get_cart_invalid_id(self):
        """TC-031 - Get cart with invalid ID returns 400."""
        response = requests.get(f"{BASE_URL}/carrinhos/invalidid123")
        assert response.status_code == 400

    def test_create_cart_without_token(self):
        """TC-032 - Create cart without token returns 401."""
        response = requests.post(f"{BASE_URL}/carrinhos", json={
            "produtos": [{"idProduto": "anyid", "quantidade": 1}]
        })
        assert response.status_code == 401

    def test_create_cart_success(self, auth_headers):
        """TC-033 - Create cart with valid product returns 201."""
        user = create_user_and_login()
        product_id = create_product(auth_headers)

        response = requests.post(f"{BASE_URL}/carrinhos",
                                 headers=user["headers"],
                                 json={
                                     "produtos": [{
                                         "idProduto": product_id,
                                         "quantidade": 1
                                     }]
                                 })
        assert response.status_code == 201
        assert "_id" in response.json()

        # Cleanup — complete purchase
        requests.delete(f"{BASE_URL}/carrinhos/concluir-compra",
                        headers=user["headers"])

    def test_create_duplicate_cart(self, auth_headers):
        """TC-034 - Create second cart for same user returns 400."""
        user = create_user_and_login()
        product_id = create_product(auth_headers)

        # First cart
        requests.post(f"{BASE_URL}/carrinhos",
                      headers=user["headers"],
                      json={"produtos": [{"idProduto": product_id, "quantidade": 1}]})

        # Second cart — should fail
        response = requests.post(f"{BASE_URL}/carrinhos",
                                 headers=user["headers"],
                                 json={"produtos": [{"idProduto": product_id,
                                                     "quantidade": 1}]})
        assert response.status_code == 400

        # Cleanup
        requests.delete(f"{BASE_URL}/carrinhos/concluir-compra",
                        headers=user["headers"])

    def test_complete_purchase(self, auth_headers):
        """TC-035 - Complete purchase (checkout) returns 200."""
        user = create_user_and_login()
        product_id = create_product(auth_headers)

        requests.post(f"{BASE_URL}/carrinhos",
                      headers=user["headers"],
                      json={"produtos": [{"idProduto": product_id, "quantidade": 1}]})

        response = requests.delete(f"{BASE_URL}/carrinhos/concluir-compra",
                                   headers=user["headers"])
        assert response.status_code == 200

    def test_cancel_purchase(self, auth_headers):
        """TC-036 - Cancel purchase returns products to stock - returns 200."""
        user = create_user_and_login()
        product_id = create_product(auth_headers)

        requests.post(f"{BASE_URL}/carrinhos",
                      headers=user["headers"],
                      json={"produtos": [{"idProduto": product_id, "quantidade": 1}]})

        response = requests.delete(f"{BASE_URL}/carrinhos/cancelar-compra",
                                   headers=user["headers"])
        assert response.status_code == 200

    def test_complete_purchase_no_cart(self):
        """TC-037 - Complete purchase with no active cart returns 200 with message."""
        user = create_user_and_login()
        response = requests.delete(f"{BASE_URL}/carrinhos/concluir-compra",
                                   headers=user["headers"])
        assert response.status_code == 200
