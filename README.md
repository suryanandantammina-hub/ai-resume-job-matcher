# AI Resume & Job Matcher

A portfolio starter project for information systems and backend engineering. This initial version provides a FastAPI REST service that compares explicit technical skill keywords in resume text and job descriptions. It is **not** a machine-learning model or a validated ATS score.

## Features
- `GET /health` service health check
- `POST /match` skill coverage, matching skills, and missing skills
- Input validation and automated API tests

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs for interactive API documentation.

## Example request
```bash
curl -X POST http://127.0.0.1:8000/match -H 'Content-Type: application/json' -d '{"resume_text":"Python SQL","job_description":"Python SQL Docker"}'
```

## Tests
```bash
pytest -q
```

## Roadmap
- Resume PDF parsing with privacy controls
- PostgreSQL persistence and migrations
- React frontend and upload experience
- Explainable NLP similarity scoring
- CI, Docker, deployment, and integration tests

## Responsible use
Do not upload real resumes containing personal information to public demo environments. Skill coverage is a simple heuristic, not a hiring recommendation.
