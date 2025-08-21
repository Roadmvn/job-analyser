from fastapi.testclient import TestClient
from app.main import app


def test_ingest_minimal():
    client = TestClient(app)
    payload = {"title": "Test Job", "url": "https://example.com", "raw_description": "kubernetes"}
    r = client.post('/ingest', json=payload)
    assert r.status_code == 200
    assert r.json().get('status') in {'inserted','updated'}


