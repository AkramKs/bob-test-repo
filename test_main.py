from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestGroceryStoreAPI:

    def test_root_endpoint(self):
        """Test the root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Grocery Store API" in data["message"]
