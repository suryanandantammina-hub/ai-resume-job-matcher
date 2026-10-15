from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel, Field
from pypdf import PdfReader
from io import BytesIO
import re

app = FastAPI(title="AI Resume & Job Matcher", version="1.0.0")
FRONTEND = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
MAX_PDF_BYTES = 5 * 1024 * 1024
SKILLS = {
    "python", "java", "sql", "react", "fastapi", "spring boot", "docker", "aws",
    "postgresql", "machine learning", "etl", "git", "javascript", "rest api",
    "pandas", "typescript", "kubernetes", "terraform", "airflow", "spark",
    "azure", "gcp", "node.js", "redis", "mongodb", "linux", "ci/cd", "pytest",
    "data engineering", "microservices", "html", "css", "flask", "django"
}
ALIASES = {
    "node.js": ["nodejs", "node js"],
    "rest api": ["restful api", "rest apis", "restful services"],
    "ci/cd": ["continuous integration", "continuous deployment"],
    "postgresql": ["postgres"],
    "javascript": ["java script"],
    "machine learning": ["ml models", "ml engineer"],
}
LEARNING_TIPS = {
    "docker": "Containerize a sample API and explain image layers.",
    "aws": "Deploy a small application using an AWS free-tier-eligible service.",
    "postgresql": "Build a relational schema and practice joins and indexing.",
    "react": "Create a component-based dashboard with API integration.",
    "kubernetes": "Deploy a small containerized service to a local cluster.",
    "sql": "Practice joins, aggregations, CTEs, and query optimization.",
}

class MatchRequest(BaseModel):
    resume_text: str = Field(min_length=1, max_length=100000)
    job_description: str = Field(min_length=1, max_length=100000)

def extract_skills(text: str) -> set[str]:
    normalized = text.casefold()
    found = set()
    for skill in SKILLS:
        variants = [skill] + ALIASES.get(skill, [])
        if any(re.search(r"(?<!\w)" + re.escape(v) + r"(?!\w)", normalized) for v in variants):
            found.add(skill)
    return found

def analyze(resume_text: str, job_description: str) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    matched = resume_skills & job_skills
    missing = job_skills - resume_skills
    score = round(100 * len(matched) / len(job_skills), 1) if job_skills else None
    return {
        "match_score": score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "recommendations": [
            {"skill": skill, "suggestion": LEARNING_TIPS.get(skill, f"Build a small project demonstrating {skill}.")}
            for skill in sorted(missing)
        ],
        "note": "Heuristic keyword coverage only; not a validated ATS score or hiring prediction."
    }

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/match")
def match(payload: MatchRequest):
    return analyze(payload.resume_text, payload.job_description)

@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/octet-stream") or not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Upload a PDF file.")
    data = await file.read(MAX_PDF_BYTES + 1)
    await file.close()
    if len(data) > MAX_PDF_BYTES:
        raise HTTPException(status_code=413, detail="PDF exceeds 5 MB limit.")
    if not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=422, detail="File is not a valid PDF.")
    try:
        reader = PdfReader(BytesIO(data), strict=True)
        if reader.is_encrypted:
            raise HTTPException(status_code=422, detail="Encrypted PDFs are not supported.")
        if len(reader.pages) > 20:
            raise HTTPException(status_code=422, detail="Maximum 20 pages.")
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=422, detail="Unable to read this PDF.")
    if not text:
        raise HTTPException(status_code=422, detail="No selectable text found. Scanned PDFs are not supported.")
    return {"text": text[:100000], "pages": len(reader.pages)}
