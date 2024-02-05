from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_crypto_prices():
    # Test with the default limit (10)
    response = client.get("/crypto-prices/")
    assert response.status_code == 200
    assert "prices" in response.json()
    assert len(response.json()["prices"]) == 10

    # Test with a custom limit (5)
    response_custom_limit = client.get("/crypto-prices/?limit=5")
    assert response_custom_limit.status_code == 200
    assert "prices" in response_custom_limit.json()
    assert len(response_custom_limit.json()["prices"]) == 5

    # Test with an invalid limit (negative value)
    response_invalid_limit = client.get("/crypto-prices/?limit=-1")
    assert response_invalid_limit.status_code == 422  # Unprocessable Entity
    assert "detail" in response_invalid_limit.json()
    assert "Limit must be greater than or equal to 0" in response_invalid_limit.json()["detail"]
