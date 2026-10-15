from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel, Field
import re

app = FastAPI(title="AI Resume & Job Matcher", version="0.2.0")
FRONTEND = Path(__file__).resolve().parent.parent / "frontend" / "index.html"

SKILLS = {"python", "java", "sql", "react", "fastapi", "spring boot", "docker", "aws", "postgresql", "machine learning", "etl", "git", "javascript", "rest api", "pandas"}

class MatchRequest(BaseModel):
    resume_text: str = Field(min_length=1, max_length=100000)
    job_description: str = Field(min_length=1, max_length=100000)

def extract_skills(text: str) -> set[str]:
    normalized = text.lower()
    return {skill for skill in SKILLS if re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", normalized)}

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/match")
def match(payload: MatchRequest):
    resume_skills = extract_skills(payload.resume_text)
    job_skills = extract_skills(payload.job_description)
    matched = resume_skills & job_skills
    missing = job_skills - resume_skills
    score = round(100 * len(matched) / len(job_skills), 1) if job_skills else None
    return {"match_score": score, "matched_skills": sorted(matched), "missing_skills": sorted(missing), "resume_skills": sorted(resume_skills), "job_skills": sorted(job_skills), "note": "Rule-based skill coverage, not an ATS prediction."}
