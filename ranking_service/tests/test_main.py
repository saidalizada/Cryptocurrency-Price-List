import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_crypto_ranks():
    # Test with a valid limit
    response_valid_limit = client.get("/crypto-ranks/?limit=5")
    assert response_valid_limit.status_code == 200
    assert "ranks" in response_valid_limit.json()
    ranks = response_valid_limit.json()["ranks"]
    assert len(ranks) == 5
    assert all("rank" in crypto for crypto in ranks)
    assert all("symbol" in crypto for crypto in ranks)

    # Test with the default limit
    response_default_limit = client.get("/crypto-ranks/")
    assert response_default_limit.status_code == 200
    assert "ranks" in response_default_limit.json()
    default_ranks = response_default_limit.json()["ranks"]
    assert len(default_ranks) == 10  # Assuming the default limit is set to 10

    # Test with an invalid limit (negative value)
    response_invalid_limit = client.get("/crypto-ranks/?limit=-1")
    assert response_invalid_limit.status_code == 422  # Unprocessable Entity
    assert "detail" in response_invalid_limit.json()
    assert "Limit must be greater than or equal to 0" in response_invalid_limit.json()["detail"]

    # Test with an invalid limit (non-integer value)
    response_non_integer_limit = client.get("/crypto-ranks/?limit=abc")
    assert response_non_integer_limit.status_code == 422  # Unprocessable Entity
    assert "detail" in response_non_integer_limit.json()
    assert "Input should be a valid integer" in response_non_integer_limit.json()["detail"][0]["msg"]

