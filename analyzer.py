import pdfplumber
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


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


def calculate_score(skills):
    total_skills = 10
    return int((len(skills) / total_skills) * 100)


def match_score(user_skills):
    jobs = pd.read_csv("data/jobs.csv")

    all_skills = set(",".join(jobs["skills"]).split(","))

    match = len(set(user_skills) & all_skills)
    total = len(all_skills)

    missing = list(all_skills - set(user_skills))

    return int((match / total) * 100), missing