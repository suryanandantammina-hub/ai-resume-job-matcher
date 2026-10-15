from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_match():
    result = client.post("/match", json={"resume_text": "Python and SQL", "job_description": "Python SQL Docker"}).json()
    assert result["match_score"] == 66.7
    assert result["missing_skills"] == ["docker"]

def test_empty_resume_rejected():
    assert client.post("/match", json={"resume_text": "", "job_description": "Python"}).status_code == 422
