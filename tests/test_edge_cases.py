from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_case_insensitive_matching():
    response = client.post("/match", json={"resume_text": "PYTHON and Sql", "job_description": "python SQL"})
    assert response.status_code == 200
    assert response.json()["match_score"] == 100.0

def test_no_known_job_skills():
    response = client.post("/match", json={"resume_text": "Python", "job_description": "communication and teamwork"})
    assert response.json()["match_score"] is None

def test_partial_word_not_matched():
    response = client.post("/match", json={"resume_text": "javascript", "job_description": "java"})
    assert response.json()["match_score"] == 0.0
