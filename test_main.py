import pytest
from unittest.mock import patch
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
        assert "<h1>Loading...</h1>" in response.text

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


class TestAIDescribeEndpoint:
    """Tests for the POST /products/ai-describe endpoint."""

    def test_ai_describe_returns_200_with_ai_description(self):
        """Test that the endpoint returns 200 and a description when the AI call succeeds."""
        ai_generated = "This luscious Organic Avocado from the Produce aisle is perfectly ripe and packed with healthy fats."
        with patch("main.generate_product_description", return_value=ai_generated) as mock_fn:
            response = client.post(
                "/products/ai-describe",
                json={"name": "Organic Avocado", "price": 2.99, "category": "Produce"},
            )
        assert response.status_code == 200
        data = response.json()
        assert "description" in data
        assert data["description"] == ai_generated
        mock_fn.assert_called_once_with(name="Organic Avocado", price=2.99, category="Produce")

    def test_ai_describe_returns_200_with_fallback_on_ai_failure(self):
        """Test that the endpoint still returns 200 when the AI call returns a fallback description."""
        fallback = "Enjoy our Organic Avocado from the Produce category, available at the great price of $2.99."
        with patch("main.generate_product_description", return_value=fallback) as mock_fn:
            response = client.post(
                "/products/ai-describe",
                json={"name": "Organic Avocado", "price": 2.99, "category": "Produce"},
            )
        assert response.status_code == 200
        data = response.json()
        assert "description" in data
        assert data["description"] == fallback
        mock_fn.assert_called_once_with(name="Organic Avocado", price=2.99, category="Produce")

    def test_ai_describe_default_category(self):
        """Test that category defaults to 'Other' when not provided."""
        ai_generated = "A wonderful product at a great value."
        with patch("main.generate_product_description", return_value=ai_generated) as mock_fn:
            response = client.post(
                "/products/ai-describe",
                json={"name": "Mystery Item", "price": 1.50},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == ai_generated
        mock_fn.assert_called_once_with(name="Mystery Item", price=1.50, category="Other")

    def test_ai_describe_invalid_price_rejected(self):
        """Test that a non-positive price is rejected with HTTP 422."""
        response = client.post(
            "/products/ai-describe",
            json={"name": "Bad Product", "price": 0},
        )
        assert response.status_code == 422

    def test_ai_describe_negative_price_rejected(self):
        """Test that a negative price is rejected with HTTP 422."""
        response = client.post(
            "/products/ai-describe",
            json={"name": "Bad Product", "price": -5.00},
        )
        assert response.status_code == 422

    def test_ai_describe_empty_name_rejected(self):
        """Test that an empty product name is rejected with HTTP 422."""
        response = client.post(
            "/products/ai-describe",
            json={"name": "", "price": 1.99},
        )
        assert response.status_code == 422

    def test_ai_describe_missing_required_fields_rejected(self):
        """Test that missing required fields (name, price) are rejected with HTTP 422."""
        # Missing price
        response = client.post("/products/ai-describe", json={"name": "Apple"})
        assert response.status_code == 422

        # Missing name
        response = client.post("/products/ai-describe", json={"price": 1.99})
        assert response.status_code == 422

    def test_ai_describe_response_has_description_key(self):
        """Test that the response body conforms to the AIDescribeResponse schema."""
        with patch("main.generate_product_description", return_value="Great product!"):
            response = client.post(
                "/products/ai-describe",
                json={"name": "Tomato", "price": 0.99, "category": "Vegetables"},
            )
        assert response.status_code == 200
        data = response.json()
        # Exactly the schema: only "description" key
        assert set(data.keys()) == {"description"}
        assert isinstance(data["description"], str)
        assert len(data["description"]) > 0

    def test_ai_describe_passes_correct_arguments_to_client(self):
        """Test that all request fields are forwarded correctly to generate_product_description."""
        with patch("main.generate_product_description", return_value="desc") as mock_fn:
            client.post(
                "/products/ai-describe",
                json={"name": "Whole Milk", "price": 3.49, "category": "Dairy"},
            )
        mock_fn.assert_called_once_with(name="Whole Milk", price=3.49, category="Dairy")
