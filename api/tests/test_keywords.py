from fastapi.testclient import TestClient
from app.main import app


def test_keywords_empty():
    client = TestClient(app)
    r = client.get('/keywords?topk=5')
    assert r.status_code == 200
    assert isinstance(r.json(), list)


