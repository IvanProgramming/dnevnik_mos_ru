import pytest
from base64 import b64encode
from json import dumps
from starlette.testclient import TestClient
from app import app

def test_fakeprovider():
    token = generate_token("Ivan", "79999999999", "Some's school")
    test_client = TestClient(app)
    test_client.get("/ping", headers={
        "authorization": f"Bearer {token}",
        "diary-alias": "fake"
    })


def generate_token(name, phone, school):
    token = "q" * 15 + ":"
    token += b64encode(dumps({
        "name": name,
        "phone_number": phone,
        "school_name": school
    }).encode("utf-8")).decode("utf-8")
