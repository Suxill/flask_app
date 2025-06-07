import pytest
from app import app  # Import your Flask app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Adjust text check to your homepage content

def test_cart_route(client):
    response = client.get('/cart')
    assert response.status_code == 200

def test_product_route(client):
    response = client.get('/products')
    assert response.status_code == 200
