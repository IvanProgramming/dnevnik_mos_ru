from starlette.testclient import TestClient

from app import app


def test_ping():
    """ Tests /ping endpoint """
    client = TestClient(app)
    resp = client.get("/ping")
    print(resp)
    assert resp.json()["data"] == {}
