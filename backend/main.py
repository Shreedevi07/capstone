# pyrefly: ignore [missing-import]
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from services.parser_service import parse_resume
from services.gemini_service import (
    parse_resume_to_json,
    match_resume_to_job,
    tailor_resume,
    generate_interview_questions
)
from services.github_service import fetch_github_data
from config import settings

app = FastAPI(title="CareerPilot AI API", version="1.0.0")

# Enable CORS for local cross-origin development (just in case)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve static directory relative to main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure static directory exists
os.makedirs(STATIC_DIR, exist_ok=True)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "model": "gemini-2.5-flash",
        "mock_fallback": settings.gemini_api_key is None
    }

@app.post("/api/parse")
async def parse_endpoint(file: UploadFile = File(...)):
    try:
        content = await file.read()
        raw_text = parse_resume(content, file.filename)
        parsed_json = parse_resume_to_json(raw_text)
        return {"raw_text": raw_text, "parsed": parsed_json}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/match")
async def match_endpoint(
    file: UploadFile | None = File(None),
    resume_text: str | None = Form(None),
    job_description: str = Form(...)
):
    try:
        raw_text = ""
        if file:
            content = await file.read()
            raw_text = parse_resume(content, file.filename)
        elif resume_text:
            raw_text = resume_text
        else:
            raise HTTPException(status_code=400, detail="Please upload a resume file or paste resume text.")
        
        match_result = match_resume_to_job(raw_text, job_description)
        return match_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/tailor")
async def tailor_endpoint(
    file: UploadFile | None = File(None),
    resume_text: str | None = Form(None),
    job_description: str = Form(...)
):
    try:
        raw_text = ""
        if file:
            content = await file.read()
            raw_text = parse_resume(content, file.filename)
        elif resume_text:
            raw_text = resume_text
        else:
            raise HTTPException(status_code=400, detail="Please upload a resume file or paste resume text.")
        
        tailored_result = tailor_resume(raw_text, job_description)
        return tailored_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/github/{username}")
async def github_endpoint(username: str):
    try:
        data = await fetch_github_data(username)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/interview")
async def interview_endpoint(
    file: UploadFile | None = File(None),
    resume_text: str | None = Form(None),
    job_description: str = Form(...)
):
    try:
        raw_text = ""
        if file:
            content = await file.read()
            raw_text = parse_resume(content, file.filename)
        elif resume_text:
            raw_text = resume_text
        else:
            raise HTTPException(status_code=400, detail="Please upload a resume file or paste resume text.")
        
        questions = generate_interview_questions(raw_text, job_description)
        return questions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Mount static files router
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        # Create a placeholder if not exists yet
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("<h1>CareerPilot AI is starting...</h1>")
    return FileResponse(index_path)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)

