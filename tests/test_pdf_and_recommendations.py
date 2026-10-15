from io import BytesIO
from fastapi.testclient import TestClient
from pypdf import PdfWriter
from app.main import app

client = TestClient(app)

def test_recommendations():
    response = client.post("/match", json={"resume_text": "Python", "job_description": "Python Docker"}).json()
    assert response["match_score"] == 50.0
    assert response["recommendations"][0]["skill"] == "docker"

def test_invalid_pdf():
    response = client.post("/extract-pdf", files={"file": ("fake.pdf", b"not a pdf", "application/pdf")})
    assert response.status_code == 422

def test_wrong_file_type():
    response = client.post("/extract-pdf", files={"file": ("fake.txt", b"hello", "text/plain")})
    assert response.status_code == 415

def test_empty_pdf():
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    output = BytesIO()
    writer.write(output)
    response = client.post("/extract-pdf", files={"file": ("blank.pdf", output.getvalue(), "application/pdf")})
    assert response.status_code == 422

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
