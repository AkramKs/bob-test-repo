import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from models import Base

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create tables
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    """Override the get_db dependency to use test database."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


class TestGroceryStoreAPI:

    def test_root_endpoint(self):
        """Test the root endpoint returns the index.html page."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert 'id="joke-banner"' in response.text
        assert "Grocery Store" in response.text

    def test_static_files_accessible(self):
        """Test that static files are served correctly."""
        # Test CSS file
        response = client.get("/static/css/styles.css")
        assert response.status_code == 200

        # Test JS file
        response = client.get("/static/js/app.js")
        assert response.status_code == 200

    def test_docs_endpoint(self):
        """Test the /docs endpoint is still accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_create_product(self):
        """Test creating a new grocery product."""
        product_data = {
            "name": "Organic Bananas",
            "description": "Fresh organic bananas from Ecuador",
            "price": 2.99,
            "category": "Fruits",
            "unit": "kg",
            "stock_quantity": 150,
            "is_available": True,
        }
        response = client.post("/products/", json=product_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Organic Bananas"
        assert data["price"] == 2.99
        assert data["category"] == "Fruits"
        assert data["unit"] == "kg"
        assert data["stock_quantity"] == 150
        assert data["is_available"] is True
        assert "id" in data

    def test_create_product_minimal_fields(self):
        """Test creating a product with only required fields."""
        product_data = {
            "name": "Milk",
            "price": 3.49,
        }
        response = client.post("/products/", json=product_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Milk"
        assert data["price"] == 3.49
        assert data["description"] == ""
        assert data["category"] == "Other"
        assert data["unit"] == "piece"
        assert data["stock_quantity"] == 0
        assert data["is_available"] is True

    def test_create_product_invalid_price(self):
        """Test creating a product with invalid (non-positive) price."""
        product_data = {
            "name": "Invalid Product",
            "price": -1.0,
        }
        response = client.post("/products/", json=product_data)
        assert response.status_code == 422

    def test_create_product_empty_name(self):
        """Test creating a product with empty name."""
        product_data = {
            "name": "",
            "price": 1.99,
        }
        response = client.post("/products/", json=product_data)
        assert response.status_code == 422

    def test_list_products(self):
        """Test listing all products."""
        # Create a couple of products
        client.post("/products/", json={"name": "Apple", "price": 1.99, "category": "Fruits"})
        client.post("/products/", json={"name": "Bread", "price": 2.49, "category": "Bakery"})

        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_products_with_category_filter(self):
        """Test listing products filtered by category."""
        client.post("/products/", json={"name": "Apple", "price": 1.99, "category": "Fruits"})
        client.post("/products/", json={"name": "Banana", "price": 0.99, "category": "Fruits"})
        client.post("/products/", json={"name": "Bread", "price": 2.49, "category": "Bakery"})

        response = client.get("/products/?category=Fruits")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        for product in data:
            assert product["category"] == "Fruits"

    def test_list_products_available_only(self):
        """Test listing only available products."""
        client.post("/products/", json={"name": "Apple", "price": 1.99, "is_available": True})
        client.post("/products/", json={"name": "Spoiled Milk", "price": 1.00, "is_available": False})

        response = client.get("/products/?available_only=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Apple"

    def test_get_product_by_id(self):
        """Test getting a single product by ID."""
        create_resp = client.post("/products/", json={"name": "Orange Juice", "price": 4.99})
        product_id = create_resp.json()["id"]

        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Orange Juice"
        assert data["price"] == 4.99
        assert data["id"] == product_id

    def test_get_product_not_found(self):
        """Test getting a non-existent product returns 404."""
        response = client.get("/products/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_product(self):
        """Test updating a product's details."""
        create_resp = client.post("/products/", json={"name": "Cheese", "price": 5.99, "stock_quantity": 20})
        product_id = create_resp.json()["id"]

        update_data = {"price": 6.49, "stock_quantity": 15}
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == 6.49
        assert data["stock_quantity"] == 15
        assert data["name"] == "Cheese"  # unchanged

    def test_update_product_not_found(self):
        """Test updating a non-existent product returns 404."""
        response = client.put("/products/99999", json={"price": 1.99})
        assert response.status_code == 404

    def test_delete_product(self):
        """Test deleting a product."""
        create_resp = client.post("/products/", json={"name": "Temporary Item", "price": 0.99})
        product_id = create_resp.json()["id"]

        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_resp = client.get(f"/products/{product_id}")
        assert get_resp.status_code == 404

    def test_delete_product_not_found(self):
        """Test deleting a non-existent product returns 404."""
        response = client.delete("/products/99999")
        assert response.status_code == 404

    def test_full_crud_flow(self):
        """Test a complete CRUD workflow."""
        # Create
        create_resp = client.post("/products/", json={
            "name": "Coffee Beans",
            "description": "Arabica coffee beans, medium roast",
            "price": 12.99,
            "category": "Beverages",
            "unit": "kg",
            "stock_quantity": 50,
            "is_available": True,
        })
        assert create_resp.status_code == 201
        product_id = create_resp.json()["id"]

        # Read
        get_resp = client.get(f"/products/{product_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == "Coffee Beans"

        # Update
        update_resp = client.put(f"/products/{product_id}", json={
            "price": 11.99,
            "stock_quantity": 45,
        })
        assert update_resp.status_code == 200
        assert update_resp.json()["price"] == 11.99

        # List
        list_resp = client.get("/products/")
        assert list_resp.status_code == 200
        assert len(list_resp.json()) == 1

        # Delete
        delete_resp = client.delete(f"/products/{product_id}")
        assert delete_resp.status_code == 204

        # Verify empty
        list_resp2 = client.get("/products/")
        assert len(list_resp2.json()) == 0
