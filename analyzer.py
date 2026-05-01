import pdfplumber
import spacy
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load NLP model
nlp = spacy.load("en_core_web_sm")


# 📄 Extract text from PDF
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# 🧠 Extract skills
def extract_skills(text):
    keywords = [
        "python", "sql", "machine learning",
        "power bi", "excel", "java", "c++"
    ]

    found_skills = []

    for word in keywords:
        if word.lower() in text.lower():
            found_skills.append(word)

    return list(set(found_skills))


# 📊 Calculate ATS score
def calculate_score(skills):
    total_skills = 10
    return int((len(skills) / total_skills) * 100)


# 🎯 Match with job dataset
def match_score(user_skills):
    jobs = pd.read_csv("data/jobs.csv")

    all_skills = set(",".join(jobs["skills"]).split(","))

    match = len(set(user_skills) & all_skills)
    total = len(all_skills)

    missing = list(all_skills - set(user_skills))

    return int((match / total) * 100), missing


# 🤖 Generate AI feedback (SAFE)
def generate_feedback(skills, missing):
    try:
        prompt = f"""
        The candidate has these skills: {skills}
        Missing skills: {missing}

        Give short, practical suggestions to improve the resume and job chances.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception:
        return f"""
⚠️ AI suggestions unavailable (quota exceeded or API issue)

👉 Improve your resume by:
- Adding missing skills: {missing}
- Including measurable achievements
- Using strong action verbs
"""


# ⭐ NEW FEATURE: Resume vs Job Description
def match_with_job_description(resume_text, job_text):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    match = len(resume_words & job_words)
    total = len(job_words)

    missing = list(job_words - resume_words)

    score = int((match / total) * 100) if total > 0 else 0

    return score, missing[:20]