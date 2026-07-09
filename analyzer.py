import os
import google.generativeai as genai
from dotenv import load_dotenv

print("Analyzer loaded successfully")

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(".env")

API_KEY = os.getenv("GEMINI_API_KEY")

print("API Key Loaded:", "Yes" if API_KEY else "No")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )

genai.configure(api_key=API_KEY)

# ==========================================
# GEMINI MODEL
# ==========================================

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================================
# RESUME ANALYZER
# ==========================================

def analyze_resume(resume_text, job_role):

    try:

        if not job_role.strip():
            job_role = "General Software Engineer"

        prompt = f"""
You are a Senior ATS Resume Reviewer,
Technical Interview Expert,
Hiring Manager,
Career Coach,
Industry Mentor,
and Resume Optimization Specialist.

Your objective is to generate the MOST DETAILED professional report possible.

==========================
RULES
==========================

• Never skip any section.
• Use Markdown headings.
• Use bullet points.
• Give professional explanations.
• Mention examples wherever applicable.
• Complete every section before stopping.
• Keep the report structured and readable.

========================================================
SECTION 1 : ATS ANALYSIS
========================================================

### ATS Score
Give a score out of 100.

### Overall Resume Summary
Write at least 5 detailed points.

### Strengths
Minimum 8 detailed strengths.

### Weaknesses
Minimum 8 detailed weaknesses.

### Missing Skills
Minimum 15 missing skills.

### Resume Improvement Suggestions
Minimum 10 professional suggestions.

### Industry Readiness

Decide whether the candidate is:

• Ready
• Partially Ready
• Not Ready

Explain your decision.

========================================================
SECTION 2 : SKILL GAP ANALYSIS
========================================================

Target Role:

{job_role}

Provide:

### Matching Skills

### Missing Skills

### Recommended Skills

### Learning Priority

Beginner

Intermediate

Advanced

========================================================
SECTION 3 : INTERVIEW QUESTIONS
========================================================

Generate EXACTLY 5 questions for EACH category.

### Technical Questions

### Scenario Based Questions

### Problem Solving Questions

### Resume Deep Dive Questions

### Project Related Questions

### Debugging Questions

### SQL Questions

### Python Questions

### Behavioral Questions

### HR Questions

========================================================
SECTION 4 : HIRING MANAGER FEEDBACK
========================================================

Provide:

### First Impression

### Major Concerns

### Strong Areas

### Hiring Recommendation

Would you hire this candidate?

Explain why.

========================================================
SECTION 5 : CAREER ROADMAP
========================================================

Provide:

### Current Skill Level

### Skills To Learn

### Recommended Certifications

### Recommended Projects

### 30-Day Roadmap

Week 1

Week 2

Week 3

Week 4

========================================================
RESUME
========================================================

{resume_text}

IMPORTANT:

Generate ALL sections.

If the response becomes long,
continue using concise bullet points instead of stopping.

Do not end early.

Finish every section completely.
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )

        return response.text.strip()

    except Exception as e:
        return f"Error analyzing resume:\n\n{str(e)}"