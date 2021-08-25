from starlette.testclient import TestClient

from app import app
from utils import generate_token


def test_request():
    token1 = generate_token("Alice", "School 1234", "700000000001")
    token1_headers = {
        "authorization": f"Bearer {token1}",
        "diary-alias": "fake"
    }
    token2 = generate_token("Bob", "School 1234", "700000000002")
    token2_headers = {
        "authorization": f"Bearer {token2}",
        "diary-alias": "fake"
    }
    client = TestClient(app)
    client.put("/friends",
               headers=token1_headers,
               json={"phone_number": "700000000002"})
    req = client.get("/friends",
                     headers=token2_headers)
    assert len(req.json()["data"]) == 1
    assert req.json()["data"][0]["status"] == "pending"
