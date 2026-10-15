# ResumeMatch — Resume & Job Skill Analyzer

A full-stack portfolio prototype built with **FastAPI, Python, and a responsive HTML/CSS/JavaScript dashboard**. Compare a resume against a job description to identify recognized technical skills, skill coverage, and learning recommendations.

> This is an explainable, rule-based keyword matcher. It is **not** a trained AI model, a validated ATS score, or a hiring prediction.

## Features
- Responsive browser dashboard at `/`
- Paste resume text and a job description
- Upload text-based PDF resumes (5 MB maximum, 20 pages)
- Recognize technical skills and common aliases
- View matched/missing skills and learning recommendations
- API docs at `/docs`, health endpoint at `/health`
- Automated Python tests and GitHub Actions configuration
- Docker support

## Run locally
Requires Python 3.12+.

```bash
git clone https://github.com/suryanandantammina-hub/ai-resume-job-matcher.git
cd ai-resume-job-matcher
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** to use the dashboard.

## Docker
```bash
docker build -t resume-match .
docker run --rm -p 8000:8000 resume-match
```

## Tests
```bash
python -m pytest -q
```

## API
- `GET /` — dashboard
- `GET /health` — service health
- `POST /match` — JSON: `{"resume_text":"Python SQL","job_description":"Python SQL Docker"}`
- `POST /extract-pdf` — multipart form file named `file`

## Architecture
Browser dashboard → FastAPI endpoints → keyword skill extractor → skill coverage and recommendations.

No database is used in this version; the server does not intentionally persist uploaded resume text. Do not upload confidential documents to any deployment you do not control. Scanned or encrypted PDFs are not supported. Uploaded PDF files are parsed in memory; for public deployment, add stronger resource isolation, rate limits, and security review.

## Project status
**Implemented in repository:** browser UI, backend matching, PDF extraction, recommendations, tests, Docker configuration.

**Not yet verified:** CI test success and public deployment. No React frontend, PostgreSQL integration, or machine-learning model is claimed.

## Potential next improvements
- Privacy-focused deployment and monitoring
- Optional database-backed user history with deletion controls
- Resume section extraction and explainable semantic similarity
- Accessibility and browser testing

## Portfolio note
This project demonstrates REST API design, Python text processing, frontend/backend integration, validation, and testing. Describe it as a **rule-based skill matching application**, not as an AI model.
