import json
import google.generativeai as genai
from config import settings

# Initialize Gemini if API key is present
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)

def get_model():
    if settings.gemini_api_key:
        return genai.GenerativeModel("gemini-2.5-flash")
    return None

def parse_resume_to_json(resume_text: str) -> dict:
    model = get_model()
    if not model:
        # High-fidelity mock parser output
        return {
            "name": "Alex Mercer",
            "email": "alex.mercer@email.com",
            "phone": "+1 (555) 019-2834",
            "skills": ["Python", "JavaScript", "React", "Node.js", "Docker", "Git", "SQL", "HTML5", "CSS3"],
            "experience": [
                {
                    "role": "Software Engineer",
                    "company": "TechSolutions Inc.",
                    "duration": "2023 - Present",
                    "highlights": [
                        "Developed high-throughput API services using Node.js, Express, and PostgreSQL.",
                        "Collaborated on containerizing local development environments using Docker.",
                        "Optimized database queries, reducing average API response times by 15%."
                    ]
                },
                {
                    "role": "Junior Developer",
                    "company": "DevBuilders Co.",
                    "duration": "2022 - 2023",
                    "highlights": [
                        "Built responsive frontend components in React.js.",
                        "Wrote unit tests achieving 85% test coverage."
                    ]
                }
            ],
            "education": [
                {
                    "degree": "B.S. in Computer Science",
                    "institution": "State University",
                    "year": "2022"
                }
            ],
            "projects": [
                {
                    "title": "E-Commerce Microservices",
                    "description": "Built a scalable purchase pipeline backend handling 500+ requests/sec with Redis caching."
                }
            ]
        }

    prompt = f"""
    Parse the following resume text into a structured JSON object.
    The output must strictly be a JSON object matching this schema:
    {{
        "name": "string or null",
        "email": "string or null",
        "phone": "string or null",
        "skills": ["string"],
        "experience": [
            {{
                "role": "string",
                "company": "string",
                "duration": "string",
                "highlights": ["string"]
            }}
        ],
        "education": [
            {{
                "degree": "string",
                "institution": "string",
                "year": "string"
            }}
        ],
        "projects": [
            {{
                "title": "string",
                "description": "string"
            }}
        ]
    }}

    Resume Text:
    {resume_text}
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini parse error: {e}")
        # Return basic parsed structure as emergency fallback
        return {"name": "Parsed Candidate", "skills": [], "experience": [], "education": [], "projects": []}

def match_resume_to_job(resume_text: str, job_description: str) -> dict:
    model = get_model()
    if not model:
        # High-fidelity mock analysis output
        return {
            "score": 75,
            "matching_skills": ["Python", "JavaScript", "React", "Docker", "Git", "SQL"],
            "missing_skills": ["FastAPI", "TypeScript", "Tailwind CSS", "Redis"],
            "suggestions": [
                "Mention Python asynchronous development (async/await) or FastAPI explicitly if you have experience.",
                "Detail project work involving TypeScript as the job description lists it as a required skill.",
                "Mention UI design or responsive development using Tailwind CSS.",
                "Add details about cache management or system scaling using Redis."
            ],
            "formatting_issues": [
                "Your resume does not list a LinkedIn profile. We recommend adding one.",
                "Ensure that your resume layout is simple and scannable by ATS software (avoid multi-column formats or heavy graphic elements)."
            ]
        }

    prompt = f"""
    Compare the candidate's resume with the job description below.
    Analyze the skill match, calculate a match percentage (0 to 100), identify missing key skills, and suggest improvements.
    The output must strictly be a JSON object matching this schema:
    {{
        "score": integer (0-100),
        "matching_skills": ["string"],
        "missing_skills": ["string"],
        "suggestions": ["string"],
        "formatting_issues": ["string"]
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini match error: {e}")
        return {"score": 50, "matching_skills": [], "missing_skills": [], "suggestions": [], "formatting_issues": []}

def tailor_resume(resume_text: str, job_description: str) -> dict:
    model = get_model()
    if not model:
        # High-fidelity mock tailored output
        return {
            "tailored_summary": "Results-driven Software Engineer with 2+ years of experience specializing in building high-performance, containerized backend services and responsive React frontends. Proficient in Python, FastAPI, and JavaScript/TypeScript, with a strong background in optimizing API latency and database queries. Dedicated to implementing scalable architectures and clean code patterns.",
            "tailored_skills": ["Python", "FastAPI", "TypeScript", "JavaScript", "React", "Node.js", "Docker", "Git", "SQL", "Redis", "Tailwind CSS"],
            "tailored_experience": [
                {
                    "role": "Software Engineer",
                    "company": "TechSolutions Inc.",
                    "duration": "2023 - Present",
                    "highlights": [
                        "Architected and developed high-throughput REST APIs using Python and FastAPI, reducing response times by 25%.",
                        "Containerized multi-service applications using Docker, improving pipeline integration and deployment workflows.",
                        "Optimized relational PostgreSQL databases and implemented caching strategies using Redis."
                    ]
                },
                {
                    "role": "Junior Developer",
                    "company": "DevBuilders Co.",
                    "duration": "2022 - 2023",
                    "highlights": [
                        "Built premium, responsive web pages and components using React and Tailwind CSS.",
                        "Wrote robust unit tests achieving 85% coverage, ensuring code stability in TypeScript workflows."
                    ]
                }
            ],
            "tailored_projects": [
                {
                    "title": "E-Commerce Microservices Integration",
                    "description": "Engineered a scalable checkout flow backend with Redis caching and FastAPI, streamlining purchase processes to support over 500 requests per second."
                }
            ]
        }

    prompt = f"""
    Analyze the resume and the job description. Rewrite/tailor the professional summary, rearrange the skills list, and rephrase experience highlights/projects to best match the job description while maintaining realistic enhancements.
    The output must strictly be a JSON object matching this schema:
    {{
        "tailored_summary": "string",
        "tailored_skills": ["string"],
        "tailored_experience": [
            {{
                "role": "string",
                "company": "string",
                "duration": "string",
                "highlights": ["string"]
            }}
        ],
        "tailored_projects": [
            {{
                "title": "string",
                "description": "string"
            }}
        ]
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini tailor error: {e}")
        return {"tailored_summary": "", "tailored_skills": [], "tailored_experience": [], "tailored_projects": []}

def generate_interview_questions(resume_text: str, job_description: str) -> list:
    model = get_model()
    if not model:
        # High-fidelity mock interview prep questions
        return [
            {
                "id": 1,
                "type": "Technical",
                "question": "Can you explain how async/await works in FastAPI and how ASGI makes it high performance?",
                "answer": "FastAPI is built on Starlette and runs on ASGI servers like Uvicorn. ASGI is asynchronous, allowing a single thread to handle concurrent client connections via Python's asyncio event loop. When code awaits an I/O operation (like database query or network request), it yields control back to the loop, letting other tasks execute in the meantime.",
                "rationale": "Tests core knowledge of FastAPI architecture, asynchronous Python, and execution models.",
                "topics": ["FastAPI", "Asynchronous Python", "Uvicorn", "ASGI"]
            },
            {
                "id": 2,
                "type": "Behavioral",
                "question": "Tell me about a time you optimized a slow API or database query. What was your process?",
                "answer": "You should use the STAR method. State the Situation (e.g., e-commerce pipeline having latency spikes), Task (reduce response time from 1.2s to sub-200ms), Action (used profiler to find heavy queries, indexed critical tables, added a Redis caching layer for product listings), and Result (achieved an 85% speedup and increased query throughput).",
                "rationale": "Examines performance profiling capability, troubleshooting skills, and impact-oriented communication.",
                "topics": ["Performance Optimization", "Redis Caching", "DB Indexing", "STAR Method"]
            },
            {
                "id": 3,
                "type": "HR",
                "question": "Why do you want to join our company as a Full-Stack Copilot Developer, and what draws you to this role?",
                "answer": "Connect your interest in LLM integration and developer productivity tools with their company's domain. Mention how you enjoy building responsive frontend interfaces (React) that interact smoothly with performant python backends (FastAPI), making a tangible difference for users.",
                "rationale": "Verifies preparation, alignment with company objectives, and soft skills.",
                "topics": ["Company Research", "Motivation", "Career Alignment"]
            }
        ]

    prompt = f"""
    Generate 5 interview questions specifically tailored for this candidate and job description.
    Include a mix of Technical, Behavioral, and HR questions.
    For each question, provide a suggested answer outline, the rationale behind asking it, and tags/topics.
    The output must strictly be a JSON array of objects matching this schema:
    [
        {{
            "id": integer,
            "type": "Technical" | "Behavioral" | "HR",
            "question": "string",
            "answer": "string",
            "rationale": "string",
            "topics": ["string"]
        }}
    ]

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini interview prep error: {e}")
        return []
